"""
Main Experiment Runner

End-to-end experiment for measuring memorization in
PLMs fine-tuned on genomic data.
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
import yaml

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data import SyntheticDNAGenerator, CanaryManager, create_dataloaders
from src.data.dataset import DNATokenizer, get_tokenizer_for_model, get_tokenizer_vocab_size
from src.models import DNABERTWrapper, DNABERTTrainer
from src.attacks import PerplexityAttack, ExtractionAttack, MembershipInferenceAttack
from src.evaluation import MemorizationMetrics, ResultVisualizer


def load_config(config_path: str) -> dict:
    """Load experiment configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def run_experiment(config: dict) -> dict:
    """
    Run the full memorization experiment.
    
    Args:
        config: Experiment configuration dictionary
        
    Returns:
        Complete experiment results
    """
    print("=" * 60)
    print("PLM MEMORIZATION EXPERIMENT")
    print("=" * 60)
    
    # Show dataset info
    data_mode = config.get('data', {}).get('mode', 'synthetic')
    print(f"\nDataset mode: {data_mode}")
    if data_mode != 'synthetic':
        real_data = config.get('data', {}).get('real_data', {})
        if data_mode == 'huggingface':
            print(f"  HuggingFace dataset: {real_data.get('hf_dataset', 'N/A')}/{real_data.get('hf_subset', 'N/A')}")
        elif data_mode == 'mixed':
            print(f"  Mixed: half real (RefSeq {real_data.get('accession', 'N/A')}), half synthetic")
        else:
            print(f"  RefSeq accession: {real_data.get('accession', 'N/A')}")
    
    # Setup output directory
    exp_name = config.get('experiment', {}).get('name', 'experiment')
    # Append dataset name if available
    data_mode = config.get('data', {}).get('mode', 'synthetic')
    if data_mode != 'synthetic':
        # Extract dataset identifier from mode or real_data
        real_data = config.get('data', {}).get('real_data', {})
        if data_mode == 'huggingface':
            dataset_id = real_data.get('hf_subset', 'hf')
        elif data_mode == 'mixed':
            dataset_id = 'mixed'
        else:
            # refseq/real mode
            accession = real_data.get('accession', '')
            if 'GCF_000005845.2' in accession:
                dataset_id = 'ecoli'
            elif 'GCF_000146045.2' in accession:
                dataset_id = 'yeast'
            else:
                dataset_id = 'real'
        exp_name = f"{exp_name}_{dataset_id}"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(config.get('experiment', {}).get('output_dir', 'outputs'))
    output_dir = output_dir / f"{exp_name}_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nOutput directory: {output_dir}")
    
    # Save config
    with open(output_dir / 'config.yaml', 'w') as f:
        yaml.dump(config, f)
    
    # ============================================
    # Phase 1: Data Preparation
    # ============================================
    print("\n" + "=" * 60)
    print("PHASE 1: Data Preparation")
    print("=" * 60)
    
    # DP (Opacus) requires consistent per-sample gradient shapes. Transformer layers
    # (e.g. MultiheadAttention) can yield [batch] vs [1] mismatches; batch_size=1 avoids this.
    if config.get('privacy', {}).get('enabled', False):
        config.setdefault('training', {})['batch_size'] = 1
        config.setdefault('training', {})['train_batch_size'] = 1
        print("DP enabled: using train batch_size=1 for Opacus compatibility.")
    
    # Create tokenizer (DNATokenizer for 'simple', HuggingFace for DNABERT-2, etc.)
    tokenizer = get_tokenizer_for_model(config)
    vocab_size = get_tokenizer_vocab_size(tokenizer)
    print(f"Tokenizer: {type(tokenizer).__name__}, vocab size: {vocab_size}")
    
    # Create dataloaders with canaries
    train_loader, test_loader, canary_manager, data_meta = create_dataloaders(
        config, tokenizer
    )
    
    print(f"Training sequences: {data_meta['num_train_sequences']}")
    print(f"Test sequences: {data_meta['num_test_sequences']}")
    print(f"Canaries inserted: {data_meta['num_canaries']}")
    
    if canary_manager:
        canary_stats = canary_manager.get_statistics()
        print(f"Canary repetition distribution: {canary_stats['repetition_distribution']}")
        canary_manager.save(str(output_dir / 'canaries.json'))
    
    # ============================================
    # Phase 2: Model Training
    # ============================================
    print("\n" + "=" * 60)
    print("PHASE 2: Model Training")
    print("=" * 60)
    
    # Initialize model (pass tokenizer so DNABERT-2 does not load it twice)
    model_config = config.get('model', {})
    model = DNABERTWrapper(
        model_name=model_config.get('name', 'simple'),
        max_length=model_config.get('max_length', 512),
        use_lora=model_config.get('use_lora', False),
        lora_config=model_config.get('lora', {}),
        device=config.get('experiment', {}).get('device', 'auto'),
        tokenizer=tokenizer,
    )
    
    print(f"Model device: {model.device}")
    print(f"Model type: {type(model.model).__name__}")
    
    # Initialize trainer
    trainer = DNABERTTrainer(
        model=model,
        config=config,
        output_dir=str(output_dir / 'checkpoints')
    )
    
    # Train model
    training_results = trainer.train(
        train_loader=train_loader,
        eval_loader=test_loader
    )
    
    print(f"\nTraining completed in {training_results['total_time']:.1f}s")
    print(f"Best validation loss: {training_results['best_val_loss']:.4f}")
    
    if training_results.get('final_epsilon'):
        print(f"Final privacy budget (ε): {training_results['final_epsilon']:.2f}")
    
    # Load best checkpoint for evaluation (so attacks run on best model, not final epoch)
    best_ckpt = Path(output_dir) / 'checkpoints' / 'best_model.pt'
    if best_ckpt.exists():
        trainer.load_checkpoint('best_model.pt')
        print("Loaded best model (by validation loss) for attack evaluation.")
    else:
        print("No best_model.pt found (e.g. save_best disabled or no eval_loader); using final model for evaluation.")
    
    # ============================================
    # Phase 3: Attack Evaluation
    # ============================================
    print("\n" + "=" * 60)
    print("PHASE 3: Attack Evaluation")
    print("=" * 60)
    
    attack_config = config.get('attacks', {})
    attack_results = {}
    
    # Perplexity Attack
    if attack_config.get('perplexity', {}).get('enabled', True):
        print("\n--- Perplexity Attack ---")
        
        canary_info = None
        if canary_manager:
            canary_info = {
                cid: c.repetitions 
                for cid, c in canary_manager.canaries.items()
            }
        
        ppl_attack = PerplexityAttack(model)
        ppl_results = ppl_attack.analyze(
            train_loader, test_loader, canary_info
        )
        
        attack_results['perplexity'] = ppl_results
        
        print(f"Train perplexity: {ppl_results['train_perplexity']['mean']:.2f}")
        print(f"Test perplexity: {ppl_results['test_perplexity']['mean']:.2f}")
        print(f"Memorization gap: {ppl_results['memorization_gap']:.2f}")
        
        if ppl_results['canary_perplexity']['mean'] > 0:
            print(f"Canary perplexity: {ppl_results['canary_perplexity']['mean']:.2f}")
    
    # Extraction Attack
    if attack_config.get('extraction', {}).get('enabled', True) and canary_manager:
        print("\n--- Extraction Attack ---")
        
        extraction_attack = ExtractionAttack(model, tokenizer, canary_manager)
        extraction_results = extraction_attack.attack_all_canaries(
            num_candidates=attack_config.get('extraction', {}).get('max_candidates', 1000)
        )
        
        attack_results['extraction'] = extraction_results
        
        print(f"Mean exposure: {extraction_results['mean_exposure']:.2f}")
        print(f"Success rate: {extraction_results['success_rate']:.2%}")
        print("\nExposure by repetition:")
        for rep, stats in extraction_results['exposure_by_repetition'].items():
            print(f"  {rep}x: {stats['mean']:.2f} ± {stats['std']:.2f}")
    
    # Membership Inference Attack
    if attack_config.get('mia', {}).get('enabled', True):
        print("\n--- Membership Inference Attack ---")
        
        mia_attack = MembershipInferenceAttack(model)
        mia_results = mia_attack.full_attack(
            train_loader, test_loader,
            threshold_percentiles=attack_config.get('mia', {}).get(
                'threshold_percentiles', [50, 75, 90, 95, 99]
            )
        )
        
        attack_results['mia'] = mia_results
        
        print(f"Likelihood ratio AUC: {mia_results['likelihood_ratio']['auc']:.3f}")
        print(f"Best threshold accuracy: {mia_results['summary']['best_threshold_accuracy']:.3f}")
        print(f"Vulnerability score: {mia_results['summary']['vulnerability_score']:.3f}")
    
    # ============================================
    # Phase 4: Metrics & Visualization
    # ============================================
    print("\n" + "=" * 60)
    print("PHASE 4: Metrics & Visualization")
    print("=" * 60)
    
    # Compute overall metrics
    metrics = MemorizationMetrics()
    metrics.set_perplexity_results(attack_results.get('perplexity'))
    metrics.set_extraction_results(attack_results.get('extraction'))
    metrics.set_mia_results(attack_results.get('mia'))
    
    metrics_summary = metrics.get_summary_dict()
    
    print(f"\nOverall memorization score: {metrics_summary['overall_memorization_score']:.3f}")
    print("\nRecommendations:")
    for rec in metrics_summary['recommendations']:
        print(f"  - {rec}")
    
    # Generate visualizations
    if config.get('visualization', {}).get('save_plots', True):
        visualizer = ResultVisualizer(
            output_dir=str(output_dir / 'plots'),
            format=config.get('visualization', {}).get('plot_format', 'png'),
            dpi=config.get('visualization', {}).get('dpi', 150)
        )
        
        visualizer.generate_all_plots(
            perplexity_results=attack_results.get('perplexity'),
            mia_results=attack_results.get('mia'),
            extraction_results=attack_results.get('extraction'),
            training_history=training_results.get('training_history'),
            metrics_summary=metrics_summary
        )
    
    # ============================================
    # Save Results
    # ============================================
    print("\n" + "=" * 60)
    print("SAVING RESULTS")
    print("=" * 60)
    
    # Compile all results
    all_results = {
        'experiment': {
            'name': exp_name,
            'timestamp': timestamp,
            'config': config
        },
        'data': {
            'num_train_sequences': data_meta['num_train_sequences'],
            'num_test_sequences': data_meta['num_test_sequences'],
            'num_canaries': data_meta['num_canaries']
        },
        'training': {
            'total_time': training_results['total_time'],
            'best_val_loss': training_results['best_val_loss'],
            'final_epsilon': training_results.get('final_epsilon'),
            'history': training_results['training_history']
        },
        'attacks': attack_results,
        'metrics': metrics_summary
    }
    
    # Save JSON results
    with open(output_dir / 'results.json', 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    
    print(f"\nResults saved to: {output_dir / 'results.json'}")
    print(f"\nExperiment complete!")
    
    return all_results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='PLM Memorization Experiment'
    )
    parser.add_argument(
        '--config', '-c',
        type=str,
        default='config/simple_model_config.yaml',
        help='Path to model config file (defines model, training, privacy, attacks)'
    )
    parser.add_argument(
        '--data', '-d',
        type=str,
        choices=['synthetic', 'ecoli', 'yeast', 'hf_gue', 'mixed'],
        default=None,
        help='Dataset to use: synthetic (default), ecoli, yeast, hf_gue, or mixed'
    )
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Run quick test with minimal settings'
    )
    
    args = parser.parse_args()
    
    # Load model config
    config_path = Path(args.config)
    if config_path.exists():
        config = load_config(str(config_path))
    else:
        print(f"Config not found at {config_path}, using defaults")
        config = {}
    
    # Load and merge dataset config if --data is provided
    if args.data:
        dataset_name = args.data
        # Map dataset name to config file (use absolute paths relative to repo root)
        repo_root = Path(__file__).parent.parent
        config_dir = repo_root / 'config'
        dataset_configs = {
            'synthetic': None,  # Use model config's data section (default synthetic)
            'ecoli': config_dir / 'ecoli_config.yaml',
            'yeast': config_dir / 'yeast_config.yaml',
            'hf_gue': config_dir / 'hf_gue_config.yaml',
            'mixed': config_dir / 'mixed_config.yaml',
        }
        
        dataset_config_path = dataset_configs.get(dataset_name)
        if dataset_config_path:
            if dataset_config_path.exists():
                dataset_config = load_config(str(dataset_config_path))
                # Merge dataset config's data section into main config
                if 'data' in dataset_config:
                    config['data'] = dataset_config['data']
                    print(f"Loaded dataset config: {dataset_name} from {dataset_config_path}")
                else:
                    print(f"Warning: Dataset config {dataset_config_path} has no 'data' section")
            else:
                print(f"Warning: Dataset config not found at {dataset_config_path}, using model config's data section")
        elif dataset_name == 'synthetic':
            # Ensure synthetic mode is set
            config.setdefault('data', {})['mode'] = 'synthetic'
            print("Using synthetic data (from model config)")
    else:
        # No --data flag: default to synthetic (only set if not already present)
        if 'data' not in config or 'mode' not in config.get('data', {}):
            config.setdefault('data', {})['mode'] = 'synthetic'
        print("No --data specified, using model config's data section")
    
    # Quick test overrides
    if args.quick:
        print("Running quick test mode...")
        config['data'] = config.get('data', {})
        config['data']['num_train_sequences'] = 100
        config['data']['num_test_sequences'] = 20
        config['data']['canaries'] = config['data'].get('canaries', {})
        config['data']['canaries']['num_canaries'] = 10
        
        config['training'] = config.get('training', {})
        config['training']['epochs'] = 5
        
        config['attacks'] = config.get('attacks', {})
        config['attacks']['extraction'] = config['attacks'].get('extraction', {})
        config['attacks']['extraction']['max_candidates'] = 100
    
    # Run experiment
    results = run_experiment(config)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
