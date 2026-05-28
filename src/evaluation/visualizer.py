"""
Result Visualizer

Creates plots and visualizations for memorization experiment results.
"""

import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import json

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    HAS_PLOTTING = True
except ImportError:
    HAS_PLOTTING = False


class ResultVisualizer:
    """
    Visualizer for memorization experiment results.
    
    Creates plots for perplexity distributions, ROC curves,
    exposure analysis, and training curves.
    """
    
    def __init__(
        self,
        output_dir: str = "outputs/plots",
        format: str = "png",
        dpi: int = 150
    ):
        """
        Initialize the visualizer.
        
        Args:
            output_dir: Directory to save plots
            format: Image format (png, pdf, svg)
            dpi: Resolution for raster formats
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.format = format
        self.dpi = dpi
        
        if HAS_PLOTTING:
            # Set style
            plt.style.use('seaborn-v0_8-whitegrid')
            sns.set_palette("husl")
    
    def _save_plot(self, name: str):
        """Save current plot to file."""
        if not HAS_PLOTTING:
            return
        path = self.output_dir / f"{name}.{self.format}"
        plt.savefig(path, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        print(f"Saved plot: {path}")
    
    def plot_perplexity_distribution(
        self,
        train_perplexities: List[float],
        test_perplexities: List[float],
        canary_perplexities: Optional[List[float]] = None
    ):
        """
        Plot perplexity distributions for train/test/canary.
        
        Args:
            train_perplexities: Perplexities of training sequences
            test_perplexities: Perplexities of test sequences
            canary_perplexities: Perplexities of canary sequences
        """
        if not HAS_PLOTTING:
            print("Matplotlib not available, skipping plot")
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot distributions
        sns.kdeplot(train_perplexities, label='Train', ax=ax, fill=True, alpha=0.3)
        sns.kdeplot(test_perplexities, label='Test', ax=ax, fill=True, alpha=0.3)
        
        if canary_perplexities:
            sns.kdeplot(canary_perplexities, label='Canaries', ax=ax, fill=True, alpha=0.3)
        
        ax.set_xlabel('Perplexity')
        ax.set_ylabel('Density')
        ax.set_title('Perplexity Distribution: Train vs Test')
        ax.legend()
        
        # Add statistics
        train_mean = np.mean(train_perplexities)
        test_mean = np.mean(test_perplexities)
        ax.axvline(train_mean, color='blue', linestyle='--', alpha=0.5, label=f'Train mean: {train_mean:.2f}')
        ax.axvline(test_mean, color='orange', linestyle='--', alpha=0.5, label=f'Test mean: {test_mean:.2f}')
        
        self._save_plot('perplexity_distribution')
    
    def plot_roc_curve(
        self,
        fpr: List[float],
        tpr: List[float],
        auc: float
    ):
        """
        Plot ROC curve for MIA.
        
        Args:
            fpr: False positive rates
            tpr: True positive rates
            auc: Area under curve
        """
        if not HAS_PLOTTING:
            return
        
        fig, ax = plt.subplots(figsize=(8, 8))
        
        ax.plot(fpr, tpr, label=f'ROC (AUC = {auc:.3f})', linewidth=2)
        ax.plot([0, 1], [0, 1], 'k--', label='Random')
        
        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.set_title('Membership Inference Attack ROC Curve')
        ax.legend(loc='lower right')
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])
        
        self._save_plot('mia_roc_curve')
    
    def plot_exposure_by_repetition(
        self,
        exposure_by_rep: Dict[int, Dict[str, float]]
    ):
        """
        Plot canary exposure by repetition count.
        
        Args:
            exposure_by_rep: Dict mapping repetition -> {'mean', 'std', 'count'}
        """
        if not HAS_PLOTTING:
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        reps = sorted(exposure_by_rep.keys())
        means = [exposure_by_rep[r]['mean'] for r in reps]
        stds = [exposure_by_rep[r]['std'] for r in reps]
        
        bars = ax.bar(range(len(reps)), means, yerr=stds, capsize=5, alpha=0.7)
        ax.set_xticks(range(len(reps)))
        ax.set_xticklabels([str(r) for r in reps])
        
        ax.set_xlabel('Number of Repetitions')
        ax.set_ylabel('Exposure Score')
        ax.set_title('Canary Exposure by Repetition Count')
        
        # Add value labels
        for bar, mean in zip(bars, means):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5,
                f'{mean:.1f}',
                ha='center',
                va='bottom'
            )
        
        self._save_plot('exposure_by_repetition')
    
    def plot_training_curve(
        self,
        history: List[Dict[str, Any]]
    ):
        """
        Plot training loss curve.
        
        Args:
            history: Training history from trainer
        """
        if not HAS_PLOTTING:
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        epochs = [h['epoch'] for h in history]
        train_losses = [h['train_loss'] for h in history]
        eval_losses = [h.get('eval_loss', None) for h in history]
        
        # Loss plot
        ax = axes[0]
        ax.plot(epochs, train_losses, label='Train Loss', marker='o')
        if any(l is not None for l in eval_losses):
            eval_losses_clean = [l for l in eval_losses if l is not None]
            ax.plot(epochs[:len(eval_losses_clean)], eval_losses_clean, 
                   label='Eval Loss', marker='s')
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Loss')
        ax.set_title('Training Loss Curve')
        ax.legend()
        
        # Perplexity plot (if available)
        ax = axes[1]
        eval_ppls = [h.get('eval_perplexity', None) for h in history]
        if any(p is not None for p in eval_ppls):
            eval_ppls_clean = [p for p in eval_ppls if p is not None]
            ax.plot(epochs[:len(eval_ppls_clean)], eval_ppls_clean, 
                   label='Eval Perplexity', marker='o', color='green')
            ax.set_xlabel('Epoch')
            ax.set_ylabel('Perplexity')
            ax.set_title('Evaluation Perplexity')
            ax.legend()
        
        plt.tight_layout()
        self._save_plot('training_curve')
    
    def plot_memorization_summary(
        self,
        metrics_summary: Dict[str, Any]
    ):
        """
        Create summary visualization of memorization metrics.
        
        Args:
            metrics_summary: Summary from MemorizationMetrics
        """
        if not HAS_PLOTTING:
            return
        
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # Overall score gauge
        ax = axes[0]
        score = metrics_summary.get('overall_memorization_score', 0)
        colors = ['green', 'yellow', 'orange', 'red']
        thresholds = [0.25, 0.5, 0.75, 1.0]
        
        wedges = ax.pie(
            [1], 
            colors=[colors[sum(score > t for t in thresholds[:-1])]],
            startangle=90,
            counterclock=False
        )
        ax.text(0, 0, f'{score:.2f}', ha='center', va='center', fontsize=24, fontweight='bold')
        ax.set_title('Overall Memorization Score')
        
        # Metrics bar chart
        ax = axes[1]
        metrics = {
            'Perplexity Gap': metrics_summary.get('perplexity_gap', 0),
            'MIA Vulnerability': metrics_summary.get('mia_vulnerability', 0),
            'Canary Exposure': metrics_summary.get('mean_canary_exposure', 0) / 128  # Normalize
        }
        
        bars = ax.bar(metrics.keys(), metrics.values(), color=['#3498db', '#e74c3c', '#2ecc71'])
        ax.set_ylabel('Score (normalized)')
        ax.set_title('Component Metrics')
        ax.set_ylim(0, max(1, max(metrics.values()) * 1.2))
        
        # Recommendations
        ax = axes[2]
        recommendations = metrics_summary.get('recommendations', [])
        ax.axis('off')
        
        text = "Recommendations:\n\n"
        for i, rec in enumerate(recommendations[:4], 1):
            text += f"{i}. {rec}\n\n"
        
        ax.text(0.1, 0.9, text, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', wrap=True)
        ax.set_title('Recommendations')
        
        plt.tight_layout()
        self._save_plot('memorization_summary')
    
    def plot_privacy_utility_tradeoff(
        self,
        results: List[Dict[str, Any]]
    ):
        """
        Plot privacy-utility tradeoff for different epsilon values.
        
        Args:
            results: List of experiment results with different epsilon values
        """
        if not HAS_PLOTTING:
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        epsilons = []
        utilities = []  # Lower eval loss = higher utility
        privacies = []  # Lower MIA AUC = better privacy
        
        for r in results:
            eps = r.get('epsilon', float('inf'))
            utility = 1 / (1 + r.get('eval_loss', 1))  # Convert to 0-1
            mia_auc = r.get('mia_auc', 0.5)
            privacy = 1 - (mia_auc - 0.5) * 2  # AUC of 0.5 = perfect privacy
            
            epsilons.append(eps)
            utilities.append(utility)
            privacies.append(privacy)
        
        # Plot
        scatter = ax.scatter(privacies, utilities, c=epsilons, cmap='viridis', s=100)
        
        for i, eps in enumerate(epsilons):
            label = f'ε={eps}' if eps != float('inf') else 'No DP'
            ax.annotate(label, (privacies[i], utilities[i]), 
                       textcoords="offset points", xytext=(5, 5))
        
        ax.set_xlabel('Privacy Score (higher = better)')
        ax.set_ylabel('Utility Score (higher = better)')
        ax.set_title('Privacy-Utility Tradeoff')
        
        plt.colorbar(scatter, label='Epsilon (ε)')
        
        self._save_plot('privacy_utility_tradeoff')
    
    def generate_all_plots(
        self,
        perplexity_results: Optional[Dict] = None,
        mia_results: Optional[Dict] = None,
        extraction_results: Optional[Dict] = None,
        training_history: Optional[List[Dict]] = None,
        metrics_summary: Optional[Dict] = None
    ):
        """
        Generate all available plots from results.
        
        Args:
            perplexity_results: From PerplexityAttack
            mia_results: From MembershipInferenceAttack
            extraction_results: From ExtractionAttack
            training_history: From DNABERTTrainer
            metrics_summary: From MemorizationMetrics
        """
        if not HAS_PLOTTING:
            print("Matplotlib not available, skipping all plots")
            return
        
        print("Generating plots...")
        
        if training_history:
            self.plot_training_curve(training_history)
        
        if mia_results and 'likelihood_ratio' in mia_results:
            lr = mia_results['likelihood_ratio']
            self.plot_roc_curve(lr['fpr'], lr['tpr'], lr['auc'])
        
        if extraction_results and 'exposure_by_repetition' in extraction_results:
            self.plot_exposure_by_repetition(
                extraction_results['exposure_by_repetition']
            )
        
        if metrics_summary:
            self.plot_memorization_summary(metrics_summary)
        
        print(f"All plots saved to: {self.output_dir}")
