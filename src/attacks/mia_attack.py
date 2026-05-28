"""
Membership Inference Attack (MIA)

Determines whether a given sequence was in the training set
based on model behavior (loss, confidence, etc.).
"""

import torch
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from torch.utils.data import DataLoader
from sklearn.metrics import roc_auc_score, roc_curve, accuracy_score
from sklearn.linear_model import LogisticRegression

from ..models.dnabert_wrapper import DNABERTWrapper


@dataclass
class MIAResult:
    """Result of membership inference attack."""
    sequence: str
    true_member: bool
    predicted_member: bool
    confidence: float  # Attack confidence
    loss: float  # Model loss on this sequence


class MembershipInferenceAttack:
    """
    Membership Inference Attack implementation.
    
    Tests whether the model memorizes training samples enough
    that an attacker can determine membership from model outputs.
    """
    
    def __init__(self, model: DNABERTWrapper):
        """
        Initialize the attack.
        
        Args:
            model: Trained model to attack
        """
        self.model = model
        self.train_losses: List[float] = []
        self.test_losses: List[float] = []
        self.results: List[MIAResult] = []
        
    def compute_losses(
        self,
        dataloader: DataLoader,
        is_train: bool = True
    ) -> List[Tuple[str, float, bool]]:
        """
        Compute losses for all sequences in a dataloader.
        
        Args:
            dataloader: Data loader with sequences
            is_train: Whether this is training data
            
        Returns:
            List of (sequence, loss, is_canary) tuples
        """
        self.model.eval_mode()
        results = []
        
        with torch.no_grad():
            for batch in dataloader:
                # Compute per-sample loss
                outputs = self.model.forward(
                    input_ids=batch['input_ids'],
                    attention_mask=batch['attention_mask'],
                    labels=batch['labels']
                )
                
                # Get per-token losses
                logits = outputs['logits']
                labels = batch['labels'].to(self.model.device)
                
                # Compute per-sample loss manually
                batch_size = logits.size(0)
                for i in range(batch_size):
                    sample_logits = logits[i, :-1, :]
                    sample_labels = labels[i, 1:]
                    
                    # Cross-entropy loss
                    loss = torch.nn.functional.cross_entropy(
                        sample_logits,
                        sample_labels,
                        reduction='mean'
                    )
                    
                    sequence = batch['sequences'][i] if 'sequences' in batch else ""
                    is_canary = batch['is_canary'][i] if 'is_canary' in batch else False
                    
                    results.append((sequence, loss.item(), is_canary))
                    
                    if is_train:
                        self.train_losses.append(loss.item())
                    else:
                        self.test_losses.append(loss.item())
        
        return results
    
    def threshold_attack(
        self,
        threshold: Optional[float] = None,
        percentile: float = 50
    ) -> Dict[str, Any]:
        """
        Simple threshold-based MIA.
        
        Predicts membership if loss < threshold.
        
        Args:
            threshold: Fixed threshold (if None, use percentile)
            percentile: Percentile of test losses to use as threshold
            
        Returns:
            Attack results dictionary
        """
        if not self.train_losses or not self.test_losses:
            raise ValueError("Must call compute_losses first")
        
        # Determine threshold
        if threshold is None:
            all_losses = self.train_losses + self.test_losses
            threshold = np.percentile(all_losses, percentile)
        
        # Compute predictions
        train_preds = [loss < threshold for loss in self.train_losses]
        test_preds = [loss < threshold for loss in self.test_losses]
        
        # Ground truth
        train_true = [True] * len(self.train_losses)
        test_true = [False] * len(self.test_losses)
        
        all_preds = train_preds + test_preds
        all_true = train_true + test_true
        
        # Compute metrics
        accuracy = accuracy_score(all_true, all_preds)
        
        # TPR and FPR
        tp = sum(1 for p, t in zip(all_preds, all_true) if p and t)
        fp = sum(1 for p, t in zip(all_preds, all_true) if p and not t)
        tn = sum(1 for p, t in zip(all_preds, all_true) if not p and not t)
        fn = sum(1 for p, t in zip(all_preds, all_true) if not p and t)
        
        tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        
        return {
            'threshold': threshold,
            'accuracy': accuracy,
            'tpr': tpr,
            'fpr': fpr,
            'precision': precision,
            'advantage': tpr - fpr  # Attacker advantage
        }
    
    def likelihood_ratio_attack(self) -> Dict[str, Any]:
        """
        Likelihood ratio based MIA.
        
        Uses the distribution of train/test losses to compute
        likelihood ratios for membership inference.
        
        Returns:
            Attack results dictionary
        """
        if not self.train_losses or not self.test_losses:
            raise ValueError("Must call compute_losses first")
        
        # Fit Gaussian to train and test distributions
        train_mean = np.mean(self.train_losses)
        train_std = np.std(self.train_losses) + 1e-8
        test_mean = np.mean(self.test_losses)
        test_std = np.std(self.test_losses) + 1e-8
        
        def gaussian_pdf(x, mean, std):
            return np.exp(-0.5 * ((x - mean) / std) ** 2) / (std * np.sqrt(2 * np.pi))
        
        # Compute likelihood ratio for each sample
        all_losses = self.train_losses + self.test_losses
        all_true = [1] * len(self.train_losses) + [0] * len(self.test_losses)
        
        likelihood_ratios = []
        for loss in all_losses:
            p_train = gaussian_pdf(loss, train_mean, train_std)
            p_test = gaussian_pdf(loss, test_mean, test_std)
            lr = p_train / (p_test + 1e-10)
            likelihood_ratios.append(lr)
        
        # Compute AUC
        auc = roc_auc_score(all_true, likelihood_ratios)
        
        # Get ROC curve
        fpr, tpr, thresholds = roc_curve(all_true, likelihood_ratios)
        
        return {
            'auc': auc,
            'fpr': fpr.tolist(),
            'tpr': tpr.tolist(),
            'train_loss_mean': train_mean,
            'train_loss_std': train_std,
            'test_loss_mean': test_mean,
            'test_loss_std': test_std,
            'loss_gap': test_mean - train_mean
        }
    
    def ml_attack(
        self,
        features: str = 'loss'
    ) -> Dict[str, Any]:
        """
        ML-based MIA using logistic regression.
        
        Args:
            features: Feature type ('loss' or 'multi')
            
        Returns:
            Attack results dictionary
        """
        if not self.train_losses or not self.test_losses:
            raise ValueError("Must call compute_losses first")
        
        # Prepare features
        if features == 'loss':
            X_train = np.array(self.train_losses[:len(self.train_losses)//2]).reshape(-1, 1)
            X_test = np.array(self.test_losses[:len(self.test_losses)//2]).reshape(-1, 1)
            
            X_val_train = np.array(self.train_losses[len(self.train_losses)//2:]).reshape(-1, 1)
            X_val_test = np.array(self.test_losses[len(self.test_losses)//2:]).reshape(-1, 1)
        else:
            raise NotImplementedError("Only 'loss' features supported")
        
        # Prepare labels
        y_train = np.concatenate([
            np.ones(len(X_train)),
            np.zeros(len(X_test))
        ])
        X_fit = np.vstack([X_train, X_test])
        
        y_val = np.concatenate([
            np.ones(len(X_val_train)),
            np.zeros(len(X_val_test))
        ])
        X_val = np.vstack([X_val_train, X_val_test])
        
        # Train logistic regression
        clf = LogisticRegression(random_state=42)
        clf.fit(X_fit, y_train)
        
        # Evaluate
        y_pred_proba = clf.predict_proba(X_val)[:, 1]
        y_pred = clf.predict(X_val)
        
        # Metrics
        accuracy = accuracy_score(y_val, y_pred)
        auc = roc_auc_score(y_val, y_pred_proba)
        
        return {
            'accuracy': accuracy,
            'auc': auc,
            'feature_type': features
        }
    
    def full_attack(
        self,
        train_loader: DataLoader,
        test_loader: DataLoader,
        threshold_percentiles: List[float] = [50, 75, 90, 95, 99]
    ) -> Dict[str, Any]:
        """
        Run full MIA evaluation with multiple methods.
        
        Args:
            train_loader: Training data loader
            test_loader: Test data loader
            threshold_percentiles: Percentiles for threshold attack
            
        Returns:
            Comprehensive attack results
        """
        # Clear previous results
        self.train_losses = []
        self.test_losses = []
        
        # Compute losses
        self.compute_losses(train_loader, is_train=True)
        self.compute_losses(test_loader, is_train=False)
        
        results = {
            'num_train_samples': len(self.train_losses),
            'num_test_samples': len(self.test_losses),
            'threshold_attacks': {},
            'likelihood_ratio': self.likelihood_ratio_attack()
        }
        
        # Multiple threshold attacks
        for percentile in threshold_percentiles:
            key = f"percentile_{percentile}"
            results['threshold_attacks'][key] = self.threshold_attack(
                percentile=percentile
            )
        
        # ML attack (if enough samples)
        if len(self.train_losses) >= 20 and len(self.test_losses) >= 20:
            results['ml_attack'] = self.ml_attack()
        
        # Summary statistics
        best_threshold_accuracy = max(
            r['accuracy'] for r in results['threshold_attacks'].values()
        )
        best_threshold_advantage = max(
            r['advantage'] for r in results['threshold_attacks'].values()
        )
        lr_auc = results['likelihood_ratio']['auc']
        
        # Compute vulnerability score directly (avoiding circular dependency)
        auc_score = (lr_auc - 0.5) * 2  # Rescale to 0-1
        advantage_score = max(0, best_threshold_advantage)
        vulnerability_score = max(0, min(1, (auc_score + advantage_score) / 2))
        
        results['summary'] = {
            'best_threshold_accuracy': best_threshold_accuracy,
            'best_threshold_advantage': best_threshold_advantage,
            'lr_auc': lr_auc,
            'vulnerability_score': vulnerability_score
        }
        
        return results
    
    def _compute_vulnerability_score(self, results: Dict) -> float:
        """
        Compute overall vulnerability score (0-1).
        
        Higher score means more vulnerable to MIA.
        """
        lr_auc = results['likelihood_ratio']['auc']
        best_advantage = results['summary']['best_threshold_advantage']
        
        # Combine metrics
        # AUC of 0.5 = random, 1.0 = perfect attack
        auc_score = (lr_auc - 0.5) * 2  # Rescale to 0-1
        
        # Advantage of 0 = no advantage, 1 = perfect
        advantage_score = max(0, best_advantage)
        
        # Average
        vulnerability = (auc_score + advantage_score) / 2
        
        return max(0, min(1, vulnerability))
