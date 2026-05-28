"""
Perplexity-based Memorization Attack

Detects memorization by comparing perplexity on training
vs. test sequences. Memorized sequences have lower perplexity.
"""

import torch
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from torch.utils.data import DataLoader

from ..models.dnabert_wrapper import DNABERTWrapper


@dataclass
class PerplexityResult:
    """Result of perplexity analysis for a sequence."""
    sequence: str
    perplexity: float
    is_train: bool
    is_canary: bool
    canary_id: Optional[str] = None
    repetitions: Optional[int] = None


class PerplexityAttack:
    """
    Perplexity-based memorization detection.
    
    Measures how confident the model is on training vs. test sequences.
    Lower perplexity on training data suggests memorization.
    """
    
    def __init__(self, model: DNABERTWrapper):
        """
        Initialize the attack.
        
        Args:
            model: Trained model to analyze
        """
        self.model = model
        self.results: List[PerplexityResult] = []
        
    def compute_perplexities(
        self,
        dataloader: DataLoader,
        is_train: bool = True,
        canary_info: Optional[Dict[str, int]] = None
    ) -> List[PerplexityResult]:
        """
        Compute perplexity for all sequences in a dataloader.
        
        Args:
            dataloader: Data loader with sequences
            is_train: Whether this is training data
            canary_info: Dict mapping canary_id -> repetitions
            
        Returns:
            List of PerplexityResult objects
        """
        self.model.eval_mode()
        results = []
        
        with torch.no_grad():
            for batch in dataloader:
                perplexities = self.model.compute_perplexity(
                    input_ids=batch['input_ids'],
                    attention_mask=batch['attention_mask']
                )
                
                # Store results for each sequence
                for idx, ppl in enumerate(perplexities):
                    canary_id = batch['canary_id'][idx] if 'canary_id' in batch else None
                    is_canary = batch['is_canary'][idx] if 'is_canary' in batch else False
                    
                    repetitions = None
                    if canary_id and canary_info:
                        repetitions = canary_info.get(canary_id)
                    
                    result = PerplexityResult(
                        sequence=batch['sequences'][idx] if 'sequences' in batch else "",
                        perplexity=ppl.item(),
                        is_train=is_train,
                        is_canary=is_canary,
                        canary_id=canary_id,
                        repetitions=repetitions
                    )
                    results.append(result)
        
        self.results.extend(results)
        return results
    
    def analyze(
        self,
        train_loader: DataLoader,
        test_loader: DataLoader,
        canary_info: Optional[Dict[str, int]] = None
    ) -> Dict[str, Any]:
        """
        Full perplexity analysis.
        
        Args:
            train_loader: Training data loader
            test_loader: Test data loader
            canary_info: Optional canary repetition info
            
        Returns:
            Analysis results dictionary
        """
        # Clear previous results
        self.results = []
        
        # Compute perplexities
        train_results = self.compute_perplexities(
            train_loader, is_train=True, canary_info=canary_info
        )
        test_results = self.compute_perplexities(
            test_loader, is_train=False, canary_info=canary_info
        )
        
        # Compute statistics
        train_ppls = [r.perplexity for r in train_results if not r.is_canary]
        test_ppls = [r.perplexity for r in test_results]
        canary_ppls = [r.perplexity for r in train_results if r.is_canary]
        
        # Group canary perplexity by repetitions
        canary_by_rep = {}
        for r in train_results:
            if r.is_canary and r.repetitions is not None:
                if r.repetitions not in canary_by_rep:
                    canary_by_rep[r.repetitions] = []
                canary_by_rep[r.repetitions].append(r.perplexity)
        
        analysis = {
            'train_perplexity': {
                'mean': np.mean(train_ppls) if train_ppls else 0,
                'std': np.std(train_ppls) if train_ppls else 0,
                'min': np.min(train_ppls) if train_ppls else 0,
                'max': np.max(train_ppls) if train_ppls else 0,
                'median': np.median(train_ppls) if train_ppls else 0,
                'per_sequence': train_ppls  # Per-sequence perplexity array
            },
            'test_perplexity': {
                'mean': np.mean(test_ppls) if test_ppls else 0,
                'std': np.std(test_ppls) if test_ppls else 0,
                'min': np.min(test_ppls) if test_ppls else 0,
                'max': np.max(test_ppls) if test_ppls else 0,
                'median': np.median(test_ppls) if test_ppls else 0,
                'per_sequence': test_ppls  # Per-sequence perplexity array
            },
            'canary_perplexity': {
                'mean': np.mean(canary_ppls) if canary_ppls else 0,
                'std': np.std(canary_ppls) if canary_ppls else 0,
                'min': np.min(canary_ppls) if canary_ppls else 0,
                'max': np.max(canary_ppls) if canary_ppls else 0,
                'per_sequence': canary_ppls  # Per-sequence perplexity array
            },
            'canary_by_repetition': {
                rep: {
                    'mean': np.mean(ppls),
                    'std': np.std(ppls),
                    'count': len(ppls),
                    'per_sequence': ppls  # Per-sequence perplexity array for this repetition count
                }
                for rep, ppls in canary_by_rep.items()
            },
            'memorization_gap': (
                np.mean(test_ppls) - np.mean(train_ppls) 
                if train_ppls and test_ppls else 0
            ),
            'num_train_samples': len(train_results),
            'num_test_samples': len(test_results),
            'num_canaries': len(canary_ppls)
        }
        
        return analysis
    
    def get_memorization_score(self) -> float:
        """
        Compute an overall memorization score.
        
        Returns a value between 0 (no memorization) and 1 (full memorization).
        Based on the gap between train and test perplexity.
        """
        train_ppls = [r.perplexity for r in self.results if r.is_train and not r.is_canary]
        test_ppls = [r.perplexity for r in self.results if not r.is_train]
        
        if not train_ppls or not test_ppls:
            return 0.0
        
        # Use ratio of means
        train_mean = np.mean(train_ppls)
        test_mean = np.mean(test_ppls)
        
        if test_mean == 0:
            return 0.0
        
        # Score based on ratio: if train_ppl << test_ppl, high memorization
        ratio = train_mean / test_mean
        
        # Convert to 0-1 score (ratio of 1 = slight memorization, ratio near 0 = high)
        score = max(0, min(1, 1 - ratio))
        
        return score
    
    def get_most_memorized(self, k: int = 10) -> List[PerplexityResult]:
        """Get the k sequences with lowest perplexity (most memorized)."""
        train_results = [r for r in self.results if r.is_train]
        sorted_results = sorted(train_results, key=lambda x: x.perplexity)
        return sorted_results[:k]
    
    def get_canary_rankings(self) -> Dict[str, int]:
        """
        Rank canaries by their perplexity among all training sequences.
        
        Returns:
            Dict mapping canary_id -> rank (1 = lowest perplexity)
        """
        train_results = [r for r in self.results if r.is_train]
        sorted_results = sorted(train_results, key=lambda x: x.perplexity)
        
        rankings = {}
        for rank, result in enumerate(sorted_results, 1):
            if result.is_canary and result.canary_id:
                rankings[result.canary_id] = rank
        
        return rankings
