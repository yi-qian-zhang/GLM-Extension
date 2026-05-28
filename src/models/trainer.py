"""
DNABERT Trainer

Training loop for DNA language models with optional
differential privacy (DP-SGD) support.
"""

import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingWarmRestarts, LinearLR
from torch.utils.data import DataLoader
from typing import Dict, List, Optional, Tuple, Any, Callable
import numpy as np
from pathlib import Path
import json
from tqdm import tqdm
import time

try:
    from opacus import PrivacyEngine
    from opacus.validators import ModuleValidator
    HAS_OPACUS = True
except ImportError:
    HAS_OPACUS = False

from .dnabert_wrapper import DNABERTWrapper


class _DPCompatLayerNorm(nn.Module):
    """
    LayerNorm implemented via GroupNorm(1, C) so per-sample gradients
    have consistent batch dimension for Opacus (avoids 'stack expects each
    tensor to be equal size' in clip_and_accumulate).
    """
    def __init__(self, normalized_shape, eps: float = 1e-5):
        super().__init__()
        if isinstance(normalized_shape, int):
            num_features = normalized_shape
        else:
            num_features = normalized_shape[0]
        self.num_features = num_features
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(num_features))
        self.bias = nn.Parameter(torch.zeros(num_features))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (B, S, H) -> (B*S, H, 1) for F.group_norm
        orig_shape = x.shape
        x = x.reshape(-1, self.num_features, 1)
        x = torch.nn.functional.group_norm(
            x, num_groups=1, weight=self.weight, bias=self.bias, eps=self.eps
        )
        return x.reshape(orig_shape)


def _replace_layernorm_for_dp(module: nn.Module) -> None:
    """Replace all nn.LayerNorm in module with _DPCompatLayerNorm (in-place)."""
    for name, child in list(module.named_children()):
        if isinstance(child, nn.LayerNorm):
            normalized_shape = child.normalized_shape
            eps = child.eps
            replacement = _DPCompatLayerNorm(normalized_shape, eps=eps)
            replacement.weight.data = child.weight.data.clone()
            replacement.bias.data = child.bias.data.clone()
            setattr(module, name, replacement)
        else:
            _replace_layernorm_for_dp(child)


class EarlyStopping:
    """Early stopping handler."""
    
    def __init__(self, patience: int = 5, min_delta: float = 0.001):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = float('inf')
        self.should_stop = False
    
    def __call__(self, val_loss: float) -> bool:
        if val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.should_stop = True
        return self.should_stop


class DNABERTTrainer:
    """
    Trainer for DNA language models.
    
    Supports standard training and DP-SGD for privacy-preserving training.
    """
    
    def __init__(
        self,
        model: DNABERTWrapper,
        config: Dict[str, Any],
        output_dir: str = "outputs"
    ):
        """
        Initialize the trainer.
        
        Args:
            model: DNABERTWrapper instance
            config: Training configuration
            output_dir: Directory for saving outputs
        """
        self.model = model
        self.config = config
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Training config
        train_config = config.get('training', {})
        self.epochs = train_config.get('epochs', 50)
        self.learning_rate = train_config.get('learning_rate', 2e-5)
        self.weight_decay = train_config.get('weight_decay', 0.01)
        self.warmup_ratio = train_config.get('warmup_ratio', 0.1)
        self.max_grad_norm = train_config.get('max_grad_norm', 1.0)
        self.gradient_accumulation_steps = train_config.get(
            'gradient_accumulation_steps', 1
        )
        # Early stopping
        es_config = train_config.get('early_stopping', {})
        self.early_stopping = None
        if es_config.get('enabled', True):
            self.early_stopping = EarlyStopping(
                patience=es_config.get('patience', 5),
                min_delta=es_config.get('min_delta', 0.001)
            )
        
        # Checkpointing
        self.save_every_n_epochs = train_config.get('save_every_n_epochs', 10)
        self.save_best = train_config.get('save_best', True)
        
        # Privacy config
        privacy_config = config.get('privacy', {})
        self.use_dp = privacy_config.get('enabled', False)
        self.epsilon = privacy_config.get('epsilon', 8.0)
        self.delta = privacy_config.get('delta', 1e-5)
        self.dp_max_grad_norm = privacy_config.get('max_grad_norm', 1.0)
        if self.use_dp and self.gradient_accumulation_steps != 1:
            self.gradient_accumulation_steps = 1  # Opacus per-sample clipping requires step every batch
        # Initialize optimizer (will be set up in train())
        self.optimizer = None
        self.scheduler = None
        self.privacy_engine = None
        
        # Training state
        self.current_epoch = 0
        self.global_step = 0
        self.best_val_loss = float('inf')
        self.training_history = []
        
    def setup_optimizer(self, train_loader: DataLoader):
        """Set up optimizer and scheduler."""
        self.optimizer = AdamW(
            self.model.parameters(),
            lr=self.learning_rate,
            weight_decay=self.weight_decay
        )
        
        # Calculate total steps
        total_steps = len(train_loader) * self.epochs // self.gradient_accumulation_steps
        warmup_steps = int(total_steps * self.warmup_ratio)
        
        # Warmup scheduler
        self.scheduler = LinearLR(
            self.optimizer,
            start_factor=0.1,
            end_factor=1.0,
            total_iters=warmup_steps
        )
        
    def setup_dp(self, train_loader: DataLoader) -> DataLoader:
        """Set up differential privacy with Opacus."""
        if not self.use_dp:
            return train_loader
            
        if not HAS_OPACUS:
            print("Warning: Opacus not installed, training without DP")
            self.use_dp = False
            # Fallback to standard optimizer/scheduler setup
            self.setup_optimizer(train_loader)
            return train_loader
        
        # Validate and fix model for DP
        model = self.model.model
        if not ModuleValidator.is_valid(model):
            model = ModuleValidator.fix(model)
            self.model.model = model.to(self.model.device)
        # Replace LayerNorm with DP-compatible variant to avoid per-sample gradient
        # shape mismatch (Opacus "stack expects each tensor to be equal size").
        _replace_layernorm_for_dp(model)
        
        # Opacus requires identical per-sample gradient shapes; Transformer layers
        # (e.g. MultiheadAttention) can break this. Force batch_size=1 so every
        # parameter has per-sample norm shape [1].
        if getattr(train_loader, "batch_size", None) != 1:
            collate_fn = getattr(train_loader, "collate_fn", None)
            train_loader = DataLoader(
                train_loader.dataset,
                batch_size=1,
                shuffle=True,
                num_workers=train_loader.num_workers,
                collate_fn=collate_fn,
            )
            print("DP: using train DataLoader with batch_size=1 for Opacus compatibility.")
        
        # (Re)create optimizer and scheduler now that the model is DP-valid.
        self.setup_optimizer(train_loader)
        
        # Create privacy engine and wrap model, optimizer, and dataloader.
        self.privacy_engine = PrivacyEngine()
        
        model, optimizer, train_loader = self.privacy_engine.make_private_with_epsilon(
            module=self.model.model,
            optimizer=self.optimizer,
            data_loader=train_loader,
            epochs=self.epochs,
            target_epsilon=self.epsilon,
            target_delta=self.delta,
            max_grad_norm=self.dp_max_grad_norm,
            poisson_sampling=False,  # Avoid empty batches; dict collate breaks Opacus empty-batch handling
        )
        
        # Compatibility shims for PyTorch >= 2.1 + Opacus:
        # - New TransformerEncoderLayer passes `is_causal` down to self_attn;
        #   older DPMultiheadAttention doesn't accept this kwarg.
        # - Some versions also lack `batch_first`, which Transformer expects.
        for module in model.modules():
            cls_name = module.__class__.__name__
            if "MultiheadAttention" in cls_name:
                # Ensure batch_first flag exists
                if not hasattr(module, "batch_first"):
                    module.batch_first = True
                
                # Patch forward to ignore unexpected is_causal kwarg (idempotent)
                if not hasattr(module, "_patched_is_causal"):
                    original_forward = module.forward
                    
                    def _forward_ignore_is_causal(*args, _orig_forward=original_forward, **kwargs):
                        kwargs.pop("is_causal", None)
                        return _orig_forward(*args, **kwargs)
                    
                    module.forward = _forward_ignore_is_causal
                    module._patched_is_causal = True
        
        # If the underlying model supports DP-related toggles (e.g., SimpleDNALM),
        # disable explicit causal and padding masks to avoid shape mismatches with
        # DP attention masks. The model will still perform full-sequence attention,
        # and the loss remains next-token prediction via label shifting.
        if hasattr(self.model.model, "use_causal_mask"):
            self.model.model.use_causal_mask = False
        if hasattr(self.model.model, "use_key_padding_mask"):
            self.model.model.use_key_padding_mask = False
        
        self.model.model = model
        self.optimizer = optimizer
        
        print(f"Training with DP: ε={self.epsilon}, δ={self.delta}")
        
        return train_loader
    
    def train_epoch(
        self,
        train_loader: DataLoader,
        epoch: int
    ) -> Dict[str, float]:
        """Train for one epoch."""
        self.model.train_mode()
        
        total_loss = 0.0
        num_batches = 0
        
        pbar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{self.epochs}")
        
        for batch_idx, batch in enumerate(pbar):
            # Forward pass
            outputs = self.model.forward(
                input_ids=batch['input_ids'],
                attention_mask=batch['attention_mask'],
                labels=batch['labels']
            )
            
            loss = outputs['loss']
            
            # Scale loss for gradient accumulation
            if self.gradient_accumulation_steps > 1:
                loss = loss / self.gradient_accumulation_steps
            
            # Backward pass
            loss.backward()
            
            # Accumulate gradients
            if (batch_idx + 1) % self.gradient_accumulation_steps == 0:
                # Clip gradients (if not using DP, which handles this)
                if not self.use_dp:
                    torch.nn.utils.clip_grad_norm_(
                        self.model.parameters(),
                        self.max_grad_norm
                    )
                
                self.optimizer.step()
                if self.scheduler is not None:
                    self.scheduler.step()
                self.optimizer.zero_grad()
                
                self.global_step += 1
            
            total_loss += loss.item() * self.gradient_accumulation_steps
            num_batches += 1
            
            # Update progress bar
            pbar.set_postfix({
                'loss': f"{total_loss / num_batches:.4f}",
                'lr': f"{self.optimizer.param_groups[0]['lr']:.2e}"
            })
        
        avg_loss = total_loss / num_batches
        
        # Get privacy spent if using DP
        epsilon_spent = None
        if self.use_dp and self.privacy_engine is not None:
            epsilon_spent = self.privacy_engine.get_epsilon(self.delta)
        
        return {
            'train_loss': avg_loss,
            'epsilon_spent': epsilon_spent
        }
    
    def evaluate(
        self,
        eval_loader: DataLoader
    ) -> Dict[str, float]:
        """Evaluate the model."""
        self.model.eval_mode()
        
        total_loss = 0.0
        total_perplexity = 0.0
        num_batches = 0
        
        with torch.no_grad():
            for batch in eval_loader:
                outputs = self.model.forward(
                    input_ids=batch['input_ids'],
                    attention_mask=batch['attention_mask'],
                    labels=batch['labels']
                )
                
                total_loss += outputs['loss'].item()
                
                # Compute perplexity
                perplexity = self.model.compute_perplexity(
                    input_ids=batch['input_ids'],
                    attention_mask=batch['attention_mask']
                )
                total_perplexity += perplexity.mean().item()
                
                num_batches += 1
        
        return {
            'eval_loss': total_loss / num_batches,
            'eval_perplexity': total_perplexity / num_batches
        }
    
    def train(
        self,
        train_loader: DataLoader,
        eval_loader: Optional[DataLoader] = None,
        callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Full training loop.
        
        Args:
            train_loader: Training data loader
            eval_loader: Optional evaluation data loader
            callback: Optional callback function called after each epoch
            
        Returns:
            Training history and final metrics
        """
        # Setup
        if self.use_dp:
            # When using DP, setup_dp will validate/fix the model, create the
            # optimizer and scheduler, and wrap everything with Opacus.
            train_loader = self.setup_dp(train_loader)
        else:
            self.setup_optimizer(train_loader)
        
        start_time = time.time()
        
        for epoch in range(self.epochs):
            self.current_epoch = epoch
            
            # Train
            train_metrics = self.train_epoch(train_loader, epoch)
            
            # Evaluate
            eval_metrics = {}
            if eval_loader is not None:
                eval_metrics = self.evaluate(eval_loader)
            
            # Combine metrics
            epoch_metrics = {
                'epoch': epoch + 1,
                **train_metrics,
                **eval_metrics,
                'time': time.time() - start_time
            }
            
            self.training_history.append(epoch_metrics)
            
            # Print metrics
            metrics_str = " | ".join(
                f"{k}: {v:.4f}" if isinstance(v, float) else f"{k}: {v}"
                for k, v in epoch_metrics.items()
            )
            print(f"Epoch {epoch+1}: {metrics_str}")
            
            # Save checkpoint (skip if save_every_n_epochs is 0)
            if self.save_every_n_epochs > 0 and (epoch + 1) % self.save_every_n_epochs == 0:
                self.save_checkpoint(f"checkpoint_epoch_{epoch+1}.pt")
            
            # Save best model
            if self.save_best and eval_loader is not None:
                if eval_metrics['eval_loss'] < self.best_val_loss:
                    self.best_val_loss = eval_metrics['eval_loss']
                    self.save_checkpoint("best_model.pt")
            
            # Early stopping
            if self.early_stopping is not None and eval_loader is not None:
                if self.early_stopping(eval_metrics['eval_loss']):
                    print(f"Early stopping at epoch {epoch+1}")
                    break
            
            # Callback
            if callback is not None:
                callback(epoch_metrics)
        
        # Save final model
        self.save_checkpoint("final_model.pt")
        self.save_training_history()
        
        return {
            'training_history': self.training_history,
            'best_val_loss': self.best_val_loss,
            'total_time': time.time() - start_time,
            'final_epsilon': train_metrics.get('epsilon_spent')
        }
    
    def save_checkpoint(self, filename: str):
        """Save a training checkpoint."""
        checkpoint_path = self.output_dir / filename
        
        checkpoint = {
            'epoch': self.current_epoch,
            'global_step': self.global_step,
            'model_state_dict': self.model.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict() if self.optimizer else None,
            'best_val_loss': self.best_val_loss,
            'config': self.config
        }
        
        torch.save(checkpoint, checkpoint_path)
        print(f"Saved checkpoint: {checkpoint_path}")
    
    def load_checkpoint(self, filename: str):
        """Load a training checkpoint. Loads to CPU first to avoid OOM when GPU is full after training."""
        checkpoint_path = self.output_dir / filename
        # Load to CPU to avoid doubling GPU memory (training leaves model on GPU)
        checkpoint = torch.load(checkpoint_path, map_location="cpu")
        self.model.model.load_state_dict(checkpoint["model_state_dict"])
        self.current_epoch = checkpoint["epoch"]
        self.global_step = checkpoint["global_step"]
        self.best_val_loss = checkpoint["best_val_loss"]
        if self.optimizer and checkpoint.get("optimizer_state_dict"):
            self.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        del checkpoint  # free CPU memory
        if hasattr(torch, "cuda") and torch.cuda.is_available():
            torch.cuda.empty_cache()
        print(f"Loaded checkpoint: {checkpoint_path}")
    
    def save_training_history(self):
        """Save training history to JSON."""
        history_path = self.output_dir / "training_history.json"
        with open(history_path, 'w') as f:
            json.dump(self.training_history, f, indent=2)
