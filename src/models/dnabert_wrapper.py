"""
DNABERT Model Wrapper

Wrapper around transformer models for DNA sequence modeling
with support for perplexity computation and sequence generation.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import CrossEntropyLoss
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

try:
    from transformers import AutoModel, AutoConfig, AutoTokenizer
    from transformers.models.bert.configuration_bert import BertConfig
    HAS_TRANSFORMERS = True
except ImportError:
    BertConfig = None
    HAS_TRANSFORMERS = False

try:
    from peft import LoraConfig, get_peft_model, TaskType
    HAS_PEFT = True
except ImportError:
    HAS_PEFT = False

# DNABERT-2 HuggingFace model ID (Genome_Factory default)
DNABERT2_MODEL_ID = "zhihan1996/DNABERT-2-117M"


def _is_dnabert2(model_name: str) -> bool:
    """Return True if model_name refers to DNABERT-2."""
    return "dnabert" in model_name.lower() or (model_name and model_name.startswith("zhihan"))


def _is_hyenadna(model_name: str) -> bool:
    """Return True if model_name refers to a HyenaDNA model."""
    return "hyenadna" in model_name.lower()


def _is_evo(model_name: str) -> bool:
    """Return True if model_name refers to an EVO model."""
    return "evo" in model_name.lower() and not model_name.lower().startswith("evol")


class DNABERT2LMHead(nn.Module):
    """
    DNABERT-2 base encoder + LM head for next-token prediction (causal LM style).
    Uses the encoder's hidden states at each position to predict the next token.
    Also used for HyenaDNA and other encoder-based models.
    """
    
    def __init__(
        self,
        encoder: nn.Module,
        hidden_size: int,
        vocab_size: int,
        pad_token_id: int = 0,
    ):
        super().__init__()
        self.encoder = encoder
        self.lm_head = nn.Linear(hidden_size, vocab_size)
        self.vocab_size = vocab_size
        self.pad_token_id = pad_token_id

    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        labels: Optional[torch.Tensor] = None,
    ) -> Dict[str, torch.Tensor]:
        # Some HF models (e.g. HyenaDNA) may not accept attention_mask; fall back gracefully.
        if attention_mask is not None:
            try:
                encoder_outputs = self.encoder(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                )
            except TypeError:
                encoder_outputs = self.encoder(input_ids=input_ids)
        else:
            encoder_outputs = self.encoder(input_ids=input_ids)
        # HF DNABERT-2 (trust_remote_code) returns a tuple, not a ModelOutput.
        # First element is the hidden states.
        if isinstance(encoder_outputs, tuple):
            hidden_states = encoder_outputs[0]
        else:
            hidden_states = encoder_outputs.last_hidden_state  # (batch, seq_len, hidden_size)
        logits = self.lm_head(hidden_states)  # (batch, seq_len, vocab_size)

        loss = None
        if labels is not None:
            shift_logits = logits[:, :-1, :].contiguous().view(-1, self.vocab_size)
            shift_labels = labels[:, 1:].contiguous().view(-1)
            loss_fct = CrossEntropyLoss(ignore_index=self.pad_token_id)
            loss = loss_fct(shift_logits, shift_labels)

        return {
            "loss": loss,
            "logits": logits,
            "hidden_states": hidden_states,
        }


class EVOLMHead(nn.Module):
    """
    EVO model + LM head for next-token prediction.
    EVO returns (embed, _) tuple, so we handle that differently.
    """
    
    def __init__(
        self,
        encoder: nn.Module,
        hidden_size: int,
        vocab_size: int,
        pad_token_id: int = 1,  # EVO uses pad_token_id=1
    ):
        super().__init__()
        self.encoder = encoder
        self.lm_head = nn.Linear(hidden_size, vocab_size)
        self.vocab_size = vocab_size
        self.pad_token_id = pad_token_id
        
        # EVO models have an unembed layer; we'll replace it with our LM head
        # But keep the original for reference
        if hasattr(encoder, 'unembed'):
            self._original_unembed = encoder.unembed
        else:
            self._original_unembed = None
    
    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        labels: Optional[torch.Tensor] = None,
    ) -> Dict[str, torch.Tensor]:
        # EVO forward returns (embed, _) tuple
        encoder_outputs = self.encoder(input_ids)
        if isinstance(encoder_outputs, tuple):
            hidden_states = encoder_outputs[0]  # (batch, seq_len, hidden_size)
        else:
            hidden_states = encoder_outputs
        
        # StripedHyena returns bfloat16; lm_head is float32. Cast to match lm_head.
        if hidden_states.dtype != self.lm_head.weight.dtype:
            hidden_states = hidden_states.to(self.lm_head.weight.dtype)
        
        logits = self.lm_head(hidden_states)  # (batch, seq_len, vocab_size)
        
        loss = None
        if labels is not None:
            shift_logits = logits[:, :-1, :].contiguous().view(-1, self.vocab_size)
            shift_labels = labels[:, 1:].contiguous().view(-1)
            loss_fct = CrossEntropyLoss(ignore_index=self.pad_token_id)
            loss = loss_fct(shift_logits, shift_labels)
        
        return {
            "loss": loss,
            "logits": logits,
            "hidden_states": hidden_states,
        }


class SimpleDNALM(nn.Module):
    """
    Simple DNA Language Model for experiments.
    
    A lightweight transformer-based model for DNA sequence modeling.
    Used when DNABERT is not available or for faster experimentation.
    """
    
    def __init__(
        self,
        vocab_size: int = 8,
        hidden_size: int = 512,
        num_layers: int = 4,
        num_heads: int = 8,
        max_length: int = 512,
        dropout: float = 0.05
    ):
        super().__init__()
        
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.max_length = max_length
        # Whether to apply an explicit causal attention mask in the Transformer.
        # This can be disabled for compatibility with some DP wrappers.
        self.use_causal_mask = True
        # Whether to pass a key padding mask into the Transformer. Can be disabled
        # under DP if the wrapped attention layer expects different batching.
        self.use_key_padding_mask = True
        
        # Embeddings
        self.token_embedding = nn.Embedding(vocab_size, hidden_size)
        self.position_embedding = nn.Embedding(max_length, hidden_size)
        self.dropout = nn.Dropout(dropout)
        
        # Transformer layers
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=hidden_size,
            nhead=num_heads,
            dim_feedforward=hidden_size * 4,
            dropout=dropout,
            activation='gelu',
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers)
        
        # Output head
        self.lm_head = nn.Linear(hidden_size, vocab_size)
        
        # Initialize weights
        self._init_weights()
        
    def _init_weights(self):
        """Initialize weights."""
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.normal_(module.weight, mean=0.0, std=0.02)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
            elif isinstance(module, nn.Embedding):
                nn.init.normal_(module.weight, mean=0.0, std=0.02)
    
    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        labels: Optional[torch.Tensor] = None
    ) -> Dict[str, torch.Tensor]:
        """
        Forward pass.
        
        Args:
            input_ids: Token IDs [batch, seq_len]
            attention_mask: Attention mask [batch, seq_len]
            labels: Labels for LM loss [batch, seq_len]
            
        Returns:
            Dictionary with logits and optional loss
        """
        batch_size, seq_len = input_ids.shape
        
        # Get embeddings
        positions = torch.arange(seq_len, device=input_ids.device).unsqueeze(0)
        x = self.token_embedding(input_ids) + self.position_embedding(positions)
        x = self.dropout(x)
        
        # Create causal mask (optional, can be disabled for DP compatibility)
        causal_mask = None
        if getattr(self, "use_causal_mask", True):
            causal_mask = torch.triu(
                torch.ones(seq_len, seq_len, device=input_ids.device),
                diagonal=1
            ).bool()
        
        # Apply transformer
        if attention_mask is not None and getattr(self, "use_key_padding_mask", True):
            # Convert attention mask to transformer format
            key_padding_mask = attention_mask == 0
        else:
            key_padding_mask = None
            
        x = self.transformer(x, mask=causal_mask, src_key_padding_mask=key_padding_mask)
        
        # Get logits
        logits = self.lm_head(x)
        
        # Compute loss if labels provided
        loss = None
        if labels is not None:
            # Shift for next-token prediction
            shift_logits = logits[:, :-1, :].contiguous()
            shift_labels = labels[:, 1:].contiguous()
            
            loss_fct = CrossEntropyLoss(ignore_index=-100)
            loss = loss_fct(
                shift_logits.view(-1, self.vocab_size),
                shift_labels.view(-1)
            )
        
        return {
            'loss': loss,
            'logits': logits,
            'hidden_states': x
        }


def _find_linear_module_names(model: nn.Module) -> List[str]:
    """Find names of all Linear modules (for LoRA target discovery)."""
    names = []
    for name, module in model.named_modules():
        if isinstance(module, nn.Linear):
            names.append(name)
    return names


class DNABERTWrapper:
    """
    Wrapper for DNA language models.
    
    Supports: simple (built-in), DNABERT-2 (HuggingFace), and other genomic models.
    DNABERT-2 is loaded with base encoder + LM head for next-token prediction,
    aligned with Genome_Factory loading (tokenizer, LoRA targets).
    """
    
    def __init__(
        self,
        model_name: str = "simple",
        max_length: int = 512,
        use_lora: bool = False,
        lora_config: Optional[Dict] = None,
        device: str = "auto",
        tokenizer: Any = None,
    ):
        """
        Initialize the model wrapper.
        
        Args:
            model_name: Model name or "simple" for built-in; use "zhihan1996/DNABERT-2-117M" for DNABERT-2
            max_length: Maximum sequence length
            use_lora: Whether to use LoRA for fine-tuning
            lora_config: LoRA configuration (r, alpha, dropout, target_modules)
            device: Device to use (auto, cuda, cpu, mps)
            tokenizer: Optional pre-loaded tokenizer (used for DNABERT-2 to avoid loading twice)
        """
        self.model_name = model_name
        self.max_length = max_length
        self.use_lora = use_lora
        
        # Set device
        if device == "auto":
            if torch.cuda.is_available():
                self.device = torch.device("cuda")
            elif torch.backends.mps.is_available():
                self.device = torch.device("mps")
            else:
                self.device = torch.device("cpu")
        else:
            self.device = torch.device(device)
        
        # Initialize model
        if model_name == "simple":
            self.model = SimpleDNALM(max_length=max_length)
            self.tokenizer = None  # Use external tokenizer
        elif HAS_TRANSFORMERS and _is_dnabert2(model_name):
            # DNABERT-2: base encoder + LM head (Genome_Factory-style loading)
            self._init_dnabert2(model_name, max_length, use_lora, lora_config or {}, tokenizer)
        elif HAS_TRANSFORMERS and _is_hyenadna(model_name):
            # HyenaDNA: base encoder + LM head (Genome_Factory-style loading)
            self._init_hyenadna(model_name, max_length, use_lora, lora_config or {}, tokenizer)
        elif _is_evo(model_name):
            # EVO: load via Evo() class, add LM head (Genome_Factory-style)
            self._init_evo(model_name, max_length, use_lora, lora_config or {}, tokenizer)
        else:
            # Default to simple model
            print(f"Model {model_name} not available, using simple DNA LM")
            self.model = SimpleDNALM(max_length=max_length)
            self.tokenizer = None
        
        # Apply LoRA for non-DNABERT-2 / non-HyenaDNA / non-EVO HF models (e.g. simple-style LoRA)
        if (
            use_lora
            and HAS_PEFT
            and not _is_dnabert2(model_name)
            and not _is_hyenadna(model_name)
            and not _is_evo(model_name)
        ):
            lora_cfg = lora_config or {}
            peft_config = LoraConfig(
                task_type=TaskType.CAUSAL_LM,
                r=lora_cfg.get('r', 8),
                lora_alpha=lora_cfg.get('alpha', 16),
                lora_dropout=lora_cfg.get('dropout', 0.1),
                target_modules=lora_cfg.get('target_modules', ['query', 'value'])
            )
            self.model = get_peft_model(self.model, peft_config)
        
        self.model = self.model.to(self.device)
    
    def _init_dnabert2(
        self,
        model_name: str,
        max_length: int,
        use_lora: bool,
        lora_config: Dict,
        tokenizer: Any,
    ) -> None:
        """Initialize DNABERT-2: load encoder, add LM head, optional LoRA (Genome_Factory-aligned)."""
        # Tokenizer (reuse if provided)
        if tokenizer is not None:
            self.tokenizer = tokenizer
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                model_max_length=max_length,
                padding_side="right",
                use_fast=True,
                trust_remote_code=True,
            )
        
        # Base encoder: load with built-in BertConfig to avoid config_class mismatch
        # (HuggingFace DNABERT-2 repo uses custom config; transformers 4.30+ rejects it.
        # See: https://huggingface.co/zhihan1996/DNABERT-2-117M/discussions/6 and
        # Genome_Factory README: use transformers==4.29.2 for other models.)
        if BertConfig is not None:
            dnabert_config = BertConfig.from_pretrained(model_name)
            encoder = AutoModel.from_pretrained(
                model_name, trust_remote_code=True, config=dnabert_config
            )
        else:
            encoder = AutoModel.from_pretrained(model_name, trust_remote_code=True)
        config = encoder.config
        hidden_size = getattr(config, "hidden_size", 768)
        vocab_size = getattr(config, "vocab_size", len(self.tokenizer))
        pad_token_id = getattr(self.tokenizer, "pad_token_id", 0)
        if pad_token_id is None:
            pad_token_id = 0
        
        # Wrap with LM head for next-token prediction
        self.model = DNABERT2LMHead(
            encoder=encoder,
            hidden_size=hidden_size,
            vocab_size=vocab_size,
            pad_token_id=pad_token_id,
        )
        
        # LoRA on encoder only (Genome_Factory target modules, excluding classifier)
        if use_lora and HAS_PEFT:
            target_modules = lora_config.get("target_modules")
            if isinstance(target_modules, list):
                # Exclude 'classifier' since we use our own lm_head
                target_modules = [m for m in target_modules if m != "classifier"]
            elif isinstance(target_modules, str):
                target_modules = [m.strip() for m in target_modules.split(",") if m.strip() != "classifier"]
            if not target_modules:
                # Default DNABERT-2 / MosaicBERT-style names (Genome_Factory uses these)
                target_modules = ["Wqkv", "dense", "gated_layers", "wo"]
            
            # Only apply to encoder; discover valid names if needed
            linear_names = _find_linear_module_names(encoder)
            valid_targets = [n for n in target_modules if any(n in ln for ln in linear_names)]
            if not valid_targets:
                valid_targets = linear_names[: min(24, len(linear_names))]  # fallback: first 24 layers
            
            peft_config = LoraConfig(
                task_type=TaskType.CAUSAL_LM,
                r=lora_config.get("r", 8),
                lora_alpha=lora_config.get("alpha", 32),
                lora_dropout=lora_config.get("dropout", 0.05),
                target_modules=valid_targets,
            )
            self.model.encoder = get_peft_model(self.model.encoder, peft_config)
            if hasattr(self.model.encoder, "print_trainable_parameters"):
                self.model.encoder.print_trainable_parameters()

    def _init_hyenadna(
        self,
        model_name: str,
        max_length: int,
        use_lora: bool,
        lora_config: Dict,
        tokenizer: Any,
    ) -> None:
        """Initialize HyenaDNA: load encoder, add LM head, optional LoRA."""
        # Tokenizer (reuse if provided)
        if tokenizer is not None:
            self.tokenizer = tokenizer
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                model_max_length=max_length,
                padding_side="right",
                use_fast=True,
                trust_remote_code=True,
            )

        # Base encoder (trust_remote_code implements HyenaDNA)
        encoder = AutoModel.from_pretrained(model_name, trust_remote_code=True)
        config = encoder.config
        hidden_size = getattr(config, "d_model", getattr(config, "hidden_size", 768))
        vocab_size = getattr(config, "vocab_size", len(self.tokenizer))
        pad_token_id = getattr(self.tokenizer, "pad_token_id", 0)
        if pad_token_id is None:
            pad_token_id = 0

        # Wrap with LM head for next-token prediction
        self.model = DNABERT2LMHead(
            encoder=encoder,
            hidden_size=hidden_size,
            vocab_size=vocab_size,
            pad_token_id=pad_token_id,
        )

        # LoRA on encoder (default: all linear layers if no specific target_modules)
        if use_lora and HAS_PEFT:
            target_modules = lora_config.get("target_modules")
            if isinstance(target_modules, list):
                target_modules = target_modules
            elif isinstance(target_modules, str) and target_modules.strip():
                # Interpret special keywords similar to Genome_Factory
                if target_modules.strip().lower() == "all":
                    target_modules = _find_linear_module_names(encoder)
                else:
                    target_modules = [m.strip() for m in target_modules.split(",")]
            else:
                target_modules = _find_linear_module_names(encoder)

            peft_config = LoraConfig(
                task_type=TaskType.CAUSAL_LM,
                r=lora_config.get("r", 8),
                lora_alpha=lora_config.get("alpha", 32),
                lora_dropout=lora_config.get("dropout", 0.05),
                target_modules=target_modules,
            )
            self.model.encoder = get_peft_model(self.model.encoder, peft_config)
            if hasattr(self.model.encoder, "print_trainable_parameters"):
                self.model.encoder.print_trainable_parameters()
    
    def _init_evo(
        self,
        model_name: str,
        max_length: int,
        use_lora: bool,
        lora_config: Dict,
        tokenizer: Any,
    ) -> None:
        """Initialize EVO: load via Evo() class, add LM head, optional LoRA (Genome_Factory-style)."""
        try:
            from evo import Evo
        except ImportError:
            raise RuntimeError(
                "EVO package not installed. Install it with:\n"
                "  git clone https://github.com/evo-design/evo.git\n"
                "  cd evo\n"
                "  pip install .\n"
                "Then return to your project directory."
            )
        
        # Load EVO model and tokenizer (Genome_Factory pattern)
        evo_model = Evo(model_name)
        encoder = evo_model.model
        evo_tokenizer = evo_model.tokenizer
        
        # Replace unembed with identity (Genome_Factory pattern for embedding extraction)
        # We'll use our own LM head instead
        class CustomEmbedding(nn.Module):
            def unembed(self, u):
                return u
        
        encoder.unembed = CustomEmbedding()
        
        # Reuse tokenizer if provided, otherwise use EVO's tokenizer
        if tokenizer is not None:
            self.tokenizer = tokenizer
        else:
            self.tokenizer = evo_tokenizer
        
        # Get model dimensions
        # EVO models typically have d_model in config or we can infer from embeddings.
        hidden_size = None
        if hasattr(encoder, "config") and getattr(encoder.config, "d_model", None) is not None:
            hidden_size = int(encoder.config.d_model)
        elif hasattr(encoder, "embed_tokens") and getattr(encoder.embed_tokens, "embedding_dim", None) is not None:
            hidden_size = int(encoder.embed_tokens.embedding_dim)
        elif hasattr(encoder, "embeddings") and getattr(encoder.embeddings, "embedding_dim", None) is not None:
            hidden_size = int(encoder.embeddings.embedding_dim)

        # As a robust fallback, infer hidden_size via a tiny forward pass.
        if hidden_size is None:
            try:
                test_ids = evo_tokenizer.tokenize("ACGT")
                if not isinstance(test_ids, (list, tuple)) or len(test_ids) == 0:
                    raise ValueError("EVO tokenizer returned empty token list.")
                test_tensor = torch.tensor([test_ids], dtype=torch.long)
                encoder.eval()
                with torch.no_grad():
                    enc_out = encoder(test_tensor)
                if isinstance(enc_out, tuple):
                    enc_out = enc_out[0]
                hidden_size = int(enc_out.shape[-1])
            except Exception:
                # Final safety fallback: use common EVO hidden size
                hidden_size = 4096
        
        # Vocab size from tokenizer or model
        vocab_size = None
        if hasattr(self.tokenizer, "__len__"):
            try:
                vocab_size = int(len(self.tokenizer))
            except Exception:
                vocab_size = None
        if vocab_size is None and hasattr(encoder, "config") and getattr(encoder.config, "vocab_size", None) is not None:
            vocab_size = int(encoder.config.vocab_size)
        if vocab_size is None:
            vocab_size = 1000  # Reasonable fallback for EVO vocab size
        
        pad_token_id = getattr(self.tokenizer, "pad_token_id", 1)  # EVO uses pad_token_id=1
        if pad_token_id is None:
            pad_token_id = 1
        
        # Wrap with LM head for next-token prediction
        self.model = EVOLMHead(
            encoder=encoder,
            hidden_size=hidden_size,
            vocab_size=vocab_size,
            pad_token_id=pad_token_id,
        )
        
        # LoRA on encoder (Genome_Factory: all linear layers or specified targets)
        if use_lora and HAS_PEFT:
            target_modules = lora_config.get("target_modules")
            if isinstance(target_modules, list):
                target_modules = target_modules
            elif isinstance(target_modules, str) and target_modules.strip():
                if target_modules.strip().lower() == "all":
                    target_modules = _find_linear_module_names(encoder)
                elif target_modules.strip().lower() == "all_in_and_out_proj":
                    # Find in_proj/out_proj layers
                    target_modules = [
                        name for name, module in encoder.named_modules()
                        if isinstance(module, nn.Linear) and ("in_proj" in name or "out_proj" in name or "score" in name)
                    ]
                else:
                    target_modules = [m.strip() for m in target_modules.split(",")]
            else:
                target_modules = _find_linear_module_names(encoder)
            
            # Default EVO LoRA targets (from Genome_Factory: Wqkv,dense,gated_layers,wo)
            if not target_modules:
                target_modules = ["Wqkv", "dense", "gated_layers", "wo"]
            
            peft_config = LoraConfig(
                task_type=TaskType.CAUSAL_LM,
                r=lora_config.get("r", 8),
                lora_alpha=lora_config.get("alpha", 32),
                lora_dropout=lora_config.get("dropout", 0.05),
                target_modules=target_modules,
            )
            self.model.encoder = get_peft_model(self.model.encoder, peft_config)
            if hasattr(self.model.encoder, "print_trainable_parameters"):
                self.model.encoder.print_trainable_parameters()
    
    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        labels: Optional[torch.Tensor] = None
    ) -> Dict[str, torch.Tensor]:
        """Forward pass through the model."""
        input_ids = input_ids.to(self.device)
        if attention_mask is not None:
            attention_mask = attention_mask.to(self.device)
        if labels is not None:
            labels = labels.to(self.device)
        
        # EVO models (StripedHyena) do not accept keyword arguments like input_ids/attention_mask.
        # Route through EVOLMHead using positional inputs only.
        if isinstance(self.model, EVOLMHead):
            return self.model(input_ids, labels=labels)
        
        # Default path (SimpleDNALM, DNABERT-2, HyenaDNA, etc.)
        return self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels,
        )
    
    def compute_loss(
        self,
        input_ids: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        labels: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """Compute the language modeling loss."""
        outputs = self.forward(input_ids, attention_mask, labels)
        return outputs['loss']
    
    def compute_perplexity(
        self,
        input_ids: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """
        Compute perplexity for sequences.
        
        Args:
            input_ids: Token IDs [batch, seq_len]
            attention_mask: Attention mask [batch, seq_len]
            
        Returns:
            Perplexity for each sequence in batch
        """
        # Move inputs to the model device so all tensors live on the same device
        input_ids = input_ids.to(self.device)
        if attention_mask is not None:
            attention_mask = attention_mask.to(self.device)

        self.model.eval()
        with torch.no_grad():
            outputs = self.forward(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=input_ids
            )
            
            logits = outputs['logits']
            
            # Compute per-token loss
            shift_logits = logits[:, :-1, :].contiguous()
            shift_labels = input_ids[:, 1:].contiguous()
            
            # Get log probabilities
            log_probs = F.log_softmax(shift_logits, dim=-1)
            
            # Gather log probs for actual tokens
            batch_size, seq_len, vocab_size = shift_logits.shape
            token_log_probs = log_probs.gather(
                dim=-1,
                index=shift_labels.unsqueeze(-1)
            ).squeeze(-1)
            
            # Mask padded positions
            if attention_mask is not None:
                mask = attention_mask[:, 1:].float()
                token_log_probs = token_log_probs * mask
                lengths = mask.sum(dim=-1)
            else:
                lengths = torch.tensor([seq_len] * batch_size, device=self.device)
            
            # Compute average negative log likelihood
            avg_nll = -token_log_probs.sum(dim=-1) / lengths
            
            # Perplexity = exp(avg_nll)
            perplexity = torch.exp(avg_nll)
            
        return perplexity
    
    def generate(
        self,
        input_ids: torch.Tensor,
        max_new_tokens: int = 50,
        temperature: float = 1.0,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None
    ) -> torch.Tensor:
        """
        Generate sequences autoregressively.
        
        Args:
            input_ids: Starting token IDs [batch, prefix_len]
            max_new_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature
            top_k: Top-k filtering
            top_p: Nucleus sampling threshold
            
        Returns:
            Generated token IDs [batch, prefix_len + max_new_tokens]
        """
        self.model.eval()
        input_ids = input_ids.to(self.device)
        generated = input_ids.clone()
        
        with torch.no_grad():
            for _ in range(max_new_tokens):
                outputs = self.forward(generated)
                next_token_logits = outputs['logits'][:, -1, :]
                
                # Apply temperature
                next_token_logits = next_token_logits / temperature
                
                # Apply top-k filtering
                if top_k is not None:
                    indices_to_remove = next_token_logits < torch.topk(
                        next_token_logits, top_k
                    )[0][..., -1, None]
                    next_token_logits[indices_to_remove] = float('-inf')
                
                # Apply top-p (nucleus) filtering
                if top_p is not None:
                    sorted_logits, sorted_indices = torch.sort(
                        next_token_logits, descending=True
                    )
                    cumulative_probs = torch.cumsum(
                        F.softmax(sorted_logits, dim=-1), dim=-1
                    )
                    sorted_indices_to_remove = cumulative_probs > top_p
                    sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[
                        ..., :-1
                    ].clone()
                    sorted_indices_to_remove[..., 0] = 0
                    
                    indices_to_remove = sorted_indices_to_remove.scatter(
                        1, sorted_indices, sorted_indices_to_remove
                    )
                    next_token_logits[indices_to_remove] = float('-inf')
                
                # Sample
                probs = F.softmax(next_token_logits, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1)
                
                generated = torch.cat([generated, next_token], dim=1)
        
        return generated
    
    def get_token_probabilities(
        self,
        input_ids: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """
        Get probability distribution over next token for each position.
        
        Returns:
            Probability tensor [batch, seq_len, vocab_size]
        """
        self.model.eval()
        with torch.no_grad():
            outputs = self.forward(input_ids, attention_mask)
            probs = F.softmax(outputs['logits'], dim=-1)
        return probs
    
    def train_mode(self):
        """Set model to training mode."""
        self.model.train()
    
    def eval_mode(self):
        """Set model to evaluation mode."""
        self.model.eval()
    
    def parameters(self):
        """Get model parameters."""
        return self.model.parameters()
    
    def save(self, path: str):
        """Save model checkpoint."""
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'model_name': self.model_name,
            'max_length': self.max_length,
            'use_lora': self.use_lora
        }, path)
    
    def load(self, path: str):
        """Load model checkpoint."""
        checkpoint = torch.load(path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
