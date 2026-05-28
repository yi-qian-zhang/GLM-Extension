# GLM Memorization

A framework for studying **memorization risks** when fine-tuning genomic language models (GLMs) on genomic data. It measures how much a DNA language model memorizes its training data using canary sequences, perplexity analysis, extraction attacks, and membership inference.

Models and training setup follow **[Genome-Factory](http://arxiv.org/abs/2509.12266)** (an integrated library for tuning, deploying, and interpreting genomic foundation models). We use the same model backends—DNABERT-2, HyenaDNA, EVO—and the same conventions for tokenizers, LoRA targets, and installation. Genome-Factory recommends **training EVO and the rest of the models in separate environments**, so we provide two requirement files: a general one for non-EVO models and a dedicated one for EVO.

## Purpose

This experiment quantifies memorization using:

- **Canary sequences** — Unique sequences inserted at known repetition counts (e.g. 1×, 5×, 10×, 20×) to measure exposure
- **Perplexity analysis** — Comparing model confidence on train vs. held-out test data
- **Extraction attacks** — Attempting to recover canaries from the model (exposure by rank)
- **Membership inference (MIA)** — Determining whether a sequence was in the training set

Results feed into an overall memorization score and mitigation recommendations (e.g. differential privacy, reduced repetition).

## Quick Start

### Installation

We use **two separate requirement files** so EVO can be trained in its own environment (as in Genome-Factory); the rest of the models use the general environment.

**Option A — General models (simple, DNABERT-2, HyenaDNA)**  
From the repository root:

```bash
pip install -r requirements.txt
```

Use this environment for `config/simple_model_config.yaml`, `config/dnabert_config.yaml`, and `config/hyenadna_config.yaml`.

**Option B — EVO only**  
Use a **separate** virtual environment and install EVO-specific dependencies:

```bash
# Create a dedicated env for EVO (recommended)
python -m venv venv_evo
source venv_evo/bin/activate   # or: venv_evo\Scripts\activate on Windows

# Install EVO from source (Genome-Factory recommendation)
git clone https://github.com/evo-design/evo.git
cd evo
pip install .
cd ..   # return to GLM-Memorization root

# Install EVO-specific requirements (flash-attn, evo-model, etc.)
pip install -r requirements_evo.txt
```

Use this environment only for `config/evo_config.yaml`. This keeps EVO’s dependencies (e.g. Flash Attention, `evo-model`) isolated from the general stack and avoids version conflicts.

### Run a quick test (minimal data, few epochs)

Uses the config’s defaults but overrides to 100 train / 20 test sequences, 10 canaries, 5 epochs:

```bash
python experiments/run_experiment.py --quick
```

If no config is given, `config/simple_model_config.yaml` is used (built-in small model, no download).

### Run a full experiment with a specific config

**Model configs** define the model, training, privacy, and attacks. **Dataset configs** define the data source. Combine them with `--data`:

**In the general environment** (after `pip install -r requirements.txt`):

```bash
# Model: Simple, Dataset: Synthetic (default)
python experiments/run_experiment.py --config config/simple_model_config.yaml

# Model: DNABERT-2, Dataset: Synthetic
python experiments/run_experiment.py --config config/dnabert_config.yaml --data synthetic

# Model: DNABERT-2, Dataset: E. coli RefSeq
python experiments/run_experiment.py --config config/dnabert_config.yaml --data ecoli

# Model: HyenaDNA, Dataset: Yeast RefSeq
python experiments/run_experiment.py --config config/hyenadna_config.yaml --data yeast

# Model: Simple, Dataset: HuggingFace GUE
python experiments/run_experiment.py --config config/simple_model_config.yaml --data hf_gue

# Model: DNABERT-2, Dataset: Mixed (half real, half synthetic)
python experiments/run_experiment.py --config config/dnabert_config.yaml --data mixed
```

**In the EVO environment** (after installing from source + `requirements_evo.txt`):

```bash
# EVO with any dataset
python experiments/run_experiment.py --config config/evo_config.yaml --data ecoli
python experiments/run_experiment.py --config config/evo_config.yaml --data yeast
python experiments/run_experiment.py --config config/evo_config.yaml --data hf_gue
```

**Available datasets:** `synthetic` (default), `ecoli`, `yeast`, `hf_gue`, `mixed`

If `--data` is not provided, the experiment uses synthetic data (from the model config's `data` section).

## Project Structure

```
GLM-Memorization/
├── config/
│   ├── simple_model_config.yaml   # Model: Built-in small transformer
│   ├── dnabert_config.yaml       # Model: DNABERT-2 117M
│   ├── hyenadna_config.yaml      # Model: HyenaDNA
│   ├── evo_config.yaml           # Model: EVO (requires evo package)
│   ├── ecoli_config.yaml        # Dataset: E. coli RefSeq (data section only)
│   ├── yeast_config.yaml         # Dataset: Yeast RefSeq (data section only)
│   ├── hf_gue_config.yaml        # Dataset: HuggingFace GUE (data section only)
│   └── mixed_config.yaml         # Dataset: Mixed real+synthetic (data section only)
├── src/
│   ├── data/
│   │   ├── synthetic_generator.py # Synthetic DNA sequence generator
│   │   ├── canary_manager.py     # Canary insertion and tracking
│   │   ├── dataset.py            # Datasets, tokenizer (HF/EVO/built-in), create_dataloaders (mode: synthetic/real/mixed)
│   │   └── real_data_loader.py   # RefSeq, HuggingFace, BED+FASTA loaders
│   ├── models/
│   │   ├── dnabert_wrapper.py    # Model wrapper (simple, DNABERT-2, HyenaDNA, EVO + LM head)
│   │   └── trainer.py            # Training loop with optional DP-SGD (Opacus)
│   ├── attacks/
│   │   ├── perplexity_attack.py  # Perplexity-based memorization
│   │   ├── extraction_attack.py  # Canary extraction / exposure
│   │   └── mia_attack.py         # Membership inference
│   └── evaluation/
│       ├── metrics.py            # Memorization metrics and recommendations
│       └── visualizer.py        # Result plots
├── experiments/
│   └── run_experiment.py         # Main experiment runner
├── tests/
│   └── test_components.py       # Unit tests
├── requirements.txt              # General env (simple, DNABERT-2, HyenaDNA)
├── requirements_evo.txt         # EVO-only env (install after evo from source)
└── README.md
```

## Supported Models

| Config | Model | Notes |
|--------|--------|------|
| `simple_model_config.yaml` | Built-in small transformer | No download; good for quick runs |
| `dnabert_config.yaml` | `zhihan1996/DNABERT-2-117M` | HuggingFace; LoRA targets for Genome_Factory-style |
| `hyenadna_config.yaml` | `LongSafari/hyenadna-medium-160k-seqlen-hf` | Long-context encoder + LM head |
| `evo_config.yaml` | EVO (e.g. evo-1-131k-base) | Use **requirements_evo.txt** in a separate env; install [evo](https://github.com/evo-design/evo) from source first |

All runs use **causal next-token prediction** (encoder + LM head). Tokenizers are chosen per model (built-in `DNATokenizer`, HuggingFace, or EVO with left padding).

## Configuration

Edit any YAML in `config/` to customize. Example layout (see `config/simple_model_config.yaml` for full options):

```yaml
experiment:
  name: "plm_memorization_simple"
  seed: 42
  output_dir: "outputs"
  device: "cpu"   # or "auto" for GPU (MPS/CUDA)

model:
  name: "simple"
  max_length: 512
  use_lora: false
  lora:
    r: 8
    alpha: 16
    target_modules: ["query", "value"]

data:
  mode: "synthetic"   # or "real" | "refseq" | "huggingface" | "mixed"; see Real Genomic Data Sources
  num_train_sequences: 1000
  num_test_sequences: 200
  sequence_length: 256
  gc_content: 0.5
  real_data: {}        # used when mode is real/refseq/huggingface (source, accession, hf_dataset, etc.)
  canaries:
    enabled: true
    num_canaries: 50
    canary_length: 64
    repetitions: [1, 5, 10, 20]

training:
  epochs: 50
  batch_size: 16
  learning_rate: 2.0e-5

privacy:
  enabled: false
  epsilon: 8.0
  delta: 1.0e-5
  max_grad_norm: 1.0
```

Parameter-efficient fine-tuning (PEFT) is supported via **LoRA** (`use_lora: true` and `lora` in config). Differential privacy uses [Opacus](https://opacus.ai/) when `privacy.enabled` is true.

## Real Genomic Data Sources

The pipeline supports **synthetic** and **real** data via `data.mode` in config: `"synthetic"` (default), `"real"`, `"refseq"`, `"huggingface"`, or `"mixed"` (half real, half synthetic). For any non-synthetic mode, sequences are loaded by `src/data/real_data_loader.py` using the `data.real_data` block (source, accession, genome_dir, stride, HuggingFace dataset/subset, or BED+FASTA paths). Dedicated configs are provided so you can run real-data experiments without editing YAML:

| Config | Data source | Notes |
|--------|-------------|--------|
| `ecoli_config.yaml` | E. coli K-12 RefSeq (GCF_000005845.2) | Downloads to `data/genomes/` on first run |
| `yeast_config.yaml` | Yeast S288C RefSeq (GCF_000146045.2) | Same as above |
| `hf_gue_config.yaml` | HuggingFace GUE (`prom_300_all`) | Caches sequences under `data/huggingface/` |

Example (combine model + dataset):

```bash
# DNABERT-2 model with E. coli RefSeq dataset
python experiments/run_experiment.py --config config/dnabert_config.yaml --data ecoli

# Simple model with HuggingFace GUE dataset
python experiments/run_experiment.py --config config/simple_model_config.yaml --data hf_gue
```

The following sources are supported via `data.real_data` when using a custom or copied config.

### Reference Genomes (NCBI RefSeq)

| Accession | Organism | Genome size |
|-----------|----------|-------------|
| **GCF_000005845.2** | *E. coli* K-12 MG1655 | ~4.6 Mbp |
| **GCF_000146045.2** | *S. cerevisiae* S288C (Yeast) | ~12.1 Mbp |
| **GCF_000001405.40** | Human GRCh38.p14 | ~3.1 Gbp |

Set `data.real_data.source: "refseq"` and `data.real_data.accession` to one of the above (or provide `data.real_data.fasta_path`). Genomes are downloaded to `data/genomes/` when not present.

- **E. coli:** [NCBI](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000005845.2/)
- **Yeast:** [NCBI](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000146045.2/)
- **Human:** [NCBI](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000001405.40/)

### HuggingFace Datasets

| Dataset | Notes |
|---------|--------|
| **leannmlindsey/GUE** | Genomic Understanding Evaluation (e.g. subset `prom_300_all`, 300bp promoter sequences). [HuggingFace](https://huggingface.co/datasets/leannmlindsey/GUE) |
| **InstaDeepAI/nucleotide_transformer_downstream_tasks_revised** | Nucleotide Transformer downstream tasks. [HuggingFace](https://huggingface.co/datasets/InstaDeepAI/nucleotide_transformer_downstream_tasks_revised) |
| **katielink/genomic-benchmarks** | Genomic sequence classification benchmarks. [HuggingFace](https://huggingface.co/datasets/katielink/genomic-benchmarks) |

Set `data.real_data.source: "huggingface"`, `data.real_data.hf_dataset`, and optionally `data.real_data.hf_subset`. Extracted sequences can be cached under `data/huggingface/`.

### BED + FASTA (functional regions)

For custom regions, set `data.real_data.source: "bed"` with `data.real_data.bed_path` and `data.real_data.fasta_path`. The pipeline extracts ACGT-only windows from the BED intervals.

### Synthetic data (baseline)

Synthetic DNA is generated by `SyntheticDNAGenerator` with configurable GC content and seed (`data.mode: "synthetic"`). Use this as a controlled baseline without external data.

## Output

Results are written to `outputs/<experiment_name>_<timestamp>/`:

- `results.json` — Full experiment results (training, attacks, metrics)
- `config.yaml` — Copy of the config used
- `canaries.json` — Canary configuration and repetition stats
- `checkpoints/` — Model checkpoints
- `plots/` — Memorization and MIA plots (if `visualization.save_plots` is true)

## Key Metrics

| Metric | Description | Interpretation |
|--------|-------------|----------------|
| **Memorization Score** | Overall risk (0–1) | >0.7 = high risk |
| **Perplexity Gap** | Train vs test perplexity | Larger = more memorization |
| **Canary Exposure** | log₂(space) − log₂(rank) | Higher = more memorized |
| **MIA AUC** | Membership inference performance | >0.7 = vulnerable |

## Privacy: Differential Privacy (DP-SGD)

To train with DP-SGD (Opacus):

```yaml
privacy:
  enabled: true
  epsilon: 8.0
  delta: 1.0e-5
  max_grad_norm: 1.0
```

Noise multiplier can be set explicitly or derived from the target ε.

## Ethical Guidelines

This code is for **responsible research** on memorization risks:

- Uses only **synthetic** or public reference data (no real human genomic data in the pipeline).
- Focuses on **measuring** memorization and exposure, not on deploying attacks.
- Supports **mitigations** (DP, canary analysis) and documents recommendations in metrics.

## Dependencies

- **General (non-EVO):** `requirements.txt` — PyTorch, Transformers, Datasets, Opacus (privacy), PEFT (LoRA), OmegaConf, PyYAML, scikit-learn, matplotlib, seaborn, tqdm, pytest, wandb, etc. Use this for the built-in simple model, DNABERT-2, and HyenaDNA.
- **EVO:** `requirements_evo.txt` — EVO-specific stack (e.g. `evo-model`, Flash Attention, compatible PyTorch/Transformers). Use in a **separate** environment after installing [evo](https://github.com/evo-design/evo) from source, as recommended by Genome-Factory.
