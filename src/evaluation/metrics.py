"""
Memorization Metrics

Comprehensive metrics for evaluating memorization in trained models.
"""

import numpy as np
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class MemorizationReport:
    """Complete memorization evaluation report."""
    overall_score: float  # 0-1 memorization score
    perplexity_gap: float
    canary_exposure: Dict[str, float]
    mia_vulnerability: float
    recommendations: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'overall_score': self.overall_score,
            'perplexity_gap': self.perplexity_gap,
            'canary_exposure': self.canary_exposure,
            'mia_vulnerability': self.mia_vulnerability,
            'recommendations': self.recommendations
        }


class MemorizationMetrics:
    """
    Comprehensive memorization metrics computation.
    
    Aggregates results from various attacks into overall
    memorization risk assessment.
    """
    
    def __init__(self):
        self.perplexity_results: Optional[Dict] = None
        self.extraction_results: Optional[Dict] = None
        self.mia_results: Optional[Dict] = None
        
    def set_perplexity_results(self, results: Dict):
        """Set perplexity attack results."""
        self.perplexity_results = results
    
    def set_extraction_results(self, results: Dict):
        """Set extraction attack results."""
        self.extraction_results = results
    
    def set_mia_results(self, results: Dict):
        """Set MIA results."""
        self.mia_results = results
    
    def compute_exposure(
        self,
        rank: int,
        sequence_length: int,
        vocab_size: int = 4
    ) -> float:
        """
        Compute exposure metric for a sequence.
        
        Exposure = log2(candidate_space) - log2(rank)
        
        Args:
            rank: Rank of target sequence among candidates
            sequence_length: Length of the sequence
            vocab_size: Vocabulary size (4 for DNA)
            
        Returns:
            Exposure score (higher = more memorized)
        """
        if rank <= 0:
            return float('inf')
        
        candidate_space = vocab_size ** sequence_length
        exposure = np.log2(candidate_space) - np.log2(rank)
        
        return exposure
    
    def compute_reconstruction_risk(
        self,
        correct_completions: int,
        total_attempts: int
    ) -> float:
        """
        Compute reconstruction risk metric.
        
        Fraction of sequences correctly completed given a prefix.
        
        Args:
            correct_completions: Number of correctly completed sequences
            total_attempts: Total completion attempts
            
        Returns:
            Reconstruction risk (0-1)
        """
        if total_attempts == 0:
            return 0.0
        return correct_completions / total_attempts
    
    def compute_overall_memorization_score(self) -> float:
        """
        Compute overall memorization score (0-1).
        
        Combines multiple metrics into single score.
        Higher score = more memorization risk.
        
        Returns:
            Overall memorization score
        """
        scores = []
        weights = []
        
        # Perplexity-based score
        if self.perplexity_results is not None:
            train_ppl = self.perplexity_results.get('train_perplexity', {}).get('mean', 0)
            test_ppl = self.perplexity_results.get('test_perplexity', {}).get('mean', 0)
            
            if test_ppl > 0:
                # Lower train/test ratio = more memorization
                ratio = train_ppl / test_ppl
                ppl_score = max(0, min(1, 1 - ratio))
                scores.append(ppl_score)
                weights.append(0.3)
        
        # Extraction-based score
        if self.extraction_results is not None:
            mean_exposure = self.extraction_results.get('mean_exposure', 0)
            max_possible_exposure = 128  # For 64-length sequence with vocab 4
            
            # Normalize exposure to 0-1
            extraction_score = min(1, mean_exposure / max_possible_exposure)
            scores.append(extraction_score)
            weights.append(0.3)
        
        # MIA-based score
        if self.mia_results is not None:
            mia_score = self.mia_results.get('summary', {}).get('vulnerability_score', 0)
            scores.append(mia_score)
            weights.append(0.4)
        
        if not scores:
            return 0.0
        
        # Weighted average
        total_weight = sum(weights)
        weighted_sum = sum(s * w for s, w in zip(scores, weights))
        
        return weighted_sum / total_weight
    
    def generate_report(self) -> MemorizationReport:
        """
        Generate comprehensive memorization report.
        
        Returns:
            MemorizationReport with all metrics and recommendations
        """
        overall_score = self.compute_overall_memorization_score()
        
        # Extract key metrics
        perplexity_gap = 0.0
        if self.perplexity_results:
            train_ppl = self.perplexity_results.get('train_perplexity', {}).get('mean', 0)
            test_ppl = self.perplexity_results.get('test_perplexity', {}).get('mean', 0)
            perplexity_gap = test_ppl - train_ppl
        
        canary_exposure = {}
        if self.extraction_results:
            individual = self.extraction_results.get('individual_results', {})
            canary_exposure = {
                cid: data['exposure'] 
                for cid, data in individual.items()
            }
        
        mia_vulnerability = 0.0
        if self.mia_results:
            mia_vulnerability = self.mia_results.get(
                'summary', {}
            ).get('vulnerability_score', 0)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            overall_score, perplexity_gap, mia_vulnerability
        )
        
        return MemorizationReport(
            overall_score=overall_score,
            perplexity_gap=perplexity_gap,
            canary_exposure=canary_exposure,
            mia_vulnerability=mia_vulnerability,
            recommendations=recommendations
        )
    
    def _generate_recommendations(
        self,
        overall_score: float,
        perplexity_gap: float,
        mia_vulnerability: float
    ) -> List[str]:
        """Generate recommendations based on metrics."""
        recommendations = []
        
        if overall_score > 0.7:
            recommendations.append(
                "HIGH RISK: Consider using differential privacy (DP-SGD) during training"
            )
            recommendations.append(
                "Reduce training epochs or increase dataset size"
            )
        elif overall_score > 0.4:
            recommendations.append(
                "MODERATE RISK: Consider adding regularization (weight decay, dropout)"
            )
            recommendations.append(
                "Monitor training for signs of overfitting"
            )
        else:
            recommendations.append(
                "LOW RISK: Current training shows acceptable memorization levels"
            )
        
        if perplexity_gap > 10:
            recommendations.append(
                "Large perplexity gap detected - model may be overfitting"
            )
        
        if mia_vulnerability > 0.6:
            recommendations.append(
                "High MIA vulnerability - consider adding noise to training"
            )
        
        return recommendations
    
    def get_summary_dict(self) -> Dict[str, Any]:
        """Get summary as dictionary for JSON export."""
        report = self.generate_report()
        
        return {
            'overall_memorization_score': report.overall_score,
            'perplexity_gap': report.perplexity_gap,
            'mia_vulnerability': report.mia_vulnerability,
            'num_canaries_evaluated': len(report.canary_exposure),
            'mean_canary_exposure': (
                np.mean(list(report.canary_exposure.values()))
                if report.canary_exposure else 0
            ),
            'recommendations': report.recommendations
        }
