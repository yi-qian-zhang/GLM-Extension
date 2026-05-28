"""
Real Genomic Data Loader

Load real DNA sequences from multiple sources:
  A) Reference genomes (NCBI FASTA files)
  B) HuggingFace datasets
  C) BED + FASTA functional regions
"""

import gzip
import logging
import os
import random
import re
import shutil
import urllib.request
from typing import Dict, List, Optional, Tuple, Any

logger = logging.getLogger(__name__)

# Known reference genome URLs
REFERENCE_GENOMES: Dict[str, Dict[str, str]] = {
    "GCF_000005845.2": {
        "name": "E. coli K-12 MG1655",
        "url": "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2_genomic.fna.gz",
    },
    "GCF_000146045.2": {
        "name": "Yeast S288C (S. cerevisiae)",
        "url": "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/146/045/GCF_000146045.2_R64/GCF_000146045.2_R64_genomic.fna.gz",
    },
    "GCF_000001405.40": {
        "name": "Human GRCh38.p14",
        "url": "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_genomic.fna.gz",
    },
}

_ACGT_RE = re.compile(r'^[ACGTacgt]+$')


def _is_acgt_only(seq: str) -> bool:
    """Check whether *seq* contains only A, C, G, T characters."""
    return bool(_ACGT_RE.match(seq))


# ------------------------------------------------------------------
# Source A: Reference Genomes (FASTA)
# ------------------------------------------------------------------

def download_reference_genome(
    accession: str,
    output_dir: str = "data/genomes",
) -> str:
    """Download a reference genome FASTA from NCBI if not already present.

    Returns the path to the uncompressed FASTA file.
    """
    if accession not in REFERENCE_GENOMES:
        raise ValueError(
            f"Unknown accession '{accession}'. "
            f"Known accessions: {list(REFERENCE_GENOMES.keys())}"
        )

    info = REFERENCE_GENOMES[accession]
    os.makedirs(output_dir, exist_ok=True)

    gz_name = os.path.basename(info["url"])
    fasta_name = gz_name.replace(".gz", "")
    fasta_path = os.path.join(output_dir, fasta_name)

    if os.path.exists(fasta_path):
        logger.info("Genome already present at %s", fasta_path)
        return fasta_path

    gz_path = os.path.join(output_dir, gz_name)
    if not os.path.exists(gz_path):
        logger.info("Downloading %s (%s) …", info["name"], info["url"])
        urllib.request.urlretrieve(info["url"], gz_path)
        logger.info("Downloaded to %s", gz_path)

    logger.info("Decompressing %s …", gz_path)
    with gzip.open(gz_path, "rb") as f_in, open(fasta_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    os.remove(gz_path)
    logger.info("Genome ready at %s", fasta_path)

    return fasta_path


def load_from_fasta(
    fasta_path: str,
    num_sequences: int,
    sequence_length: int = 256,
    stride: int = 256,
    seed: int = 42,
) -> List[str]:
    """Extract fixed-length windows from a FASTA file.

    1. Parse every record with BioPython ``SeqIO``.
    2. Slide a window of *sequence_length* bp with step *stride*.
    3. Keep only ACGT-only windows.
    4. Randomly sample *num_sequences* windows.
    """
    from Bio import SeqIO

    windows: List[str] = []
    for record in SeqIO.parse(fasta_path, "fasta"):
        seq = str(record.seq).upper()
        for start in range(0, len(seq) - sequence_length + 1, stride):
            window = seq[start : start + sequence_length]
            if len(window) == sequence_length and _is_acgt_only(window):
                windows.append(window)

    if len(windows) == 0:
        raise RuntimeError(
            f"No valid {sequence_length}bp ACGT-only windows found in {fasta_path}"
        )

    logger.info(
        "Extracted %d valid %dbp windows from %s",
        len(windows), sequence_length, fasta_path,
    )

    rng = random.Random(seed)
    if len(windows) <= num_sequences:
        logger.warning(
            "Only %d windows available (requested %d); returning all",
            len(windows), num_sequences,
        )
        rng.shuffle(windows)
        return windows

    return rng.sample(windows, num_sequences)


# ------------------------------------------------------------------
# Source B: HuggingFace Datasets
# ------------------------------------------------------------------

def load_from_huggingface(
    dataset_name: str,
    subset: Optional[str] = None,
    split: str = "train",
    num_sequences: int = 1000,
    sequence_length: int = 256,
    seed: int = 42,
    sequence_column: str = "sequence",
) -> List[str]:
    """Load sequences from a HuggingFace dataset.

    Sequences longer than *sequence_length* are center-cropped; sequences
    shorter are skipped.  Only ACGT-only sequences are kept.
    """
    from datasets import load_dataset

    logger.info(
        "Loading HuggingFace dataset %s (subset=%s, split=%s) …",
        dataset_name, subset, split,
    )
    kwargs: Dict[str, Any] = {}
    if subset is not None:
        kwargs["name"] = subset
    ds = load_dataset(dataset_name, split=split, **kwargs)

    # Try common column names if the specified one is missing
    col = sequence_column
    if col not in ds.column_names:
        for candidate in ("sequence", "seq", "text", "dna"):
            if candidate in ds.column_names:
                col = candidate
                break
        else:
            raise ValueError(
                f"No sequence column found in dataset. "
                f"Columns: {ds.column_names}"
            )

    sequences: List[str] = []
    for row in ds:
        seq = str(row[col]).upper()
        if len(seq) < sequence_length:
            continue
        if len(seq) > sequence_length:
            start = (len(seq) - sequence_length) // 2
            seq = seq[start : start + sequence_length]
        if _is_acgt_only(seq):
            sequences.append(seq)

    if len(sequences) == 0:
        raise RuntimeError(
            f"No valid {sequence_length}bp ACGT-only sequences found in "
            f"{dataset_name}/{subset}"
        )

    logger.info(
        "Found %d valid %dbp sequences from HuggingFace dataset",
        len(sequences), sequence_length,
    )

    rng = random.Random(seed)
    if len(sequences) <= num_sequences:
        logger.warning(
            "Only %d sequences available (requested %d); returning all",
            len(sequences), num_sequences,
        )
        rng.shuffle(sequences)
        return sequences

    return rng.sample(sequences, num_sequences)


# ------------------------------------------------------------------
# Source C: BED + FASTA functional regions
# ------------------------------------------------------------------

def load_from_bed(
    bed_path: str,
    fasta_path: str,
    num_sequences: int = 1000,
    sequence_length: int = 256,
    seed: int = 42,
) -> List[str]:
    """Extract sequences from genomic regions defined in a BED file.

    Requires BioPython for FASTA indexing.
    """
    from Bio import SeqIO

    # Index the FASTA file for random access
    genome: Dict[str, str] = {}
    for record in SeqIO.parse(fasta_path, "fasta"):
        genome[record.id] = str(record.seq).upper()

    sequences: List[str] = []
    with open(bed_path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("track"):
                continue
            parts = line.split("\t")
            if len(parts) < 3:
                continue
            chrom, start, end = parts[0], int(parts[1]), int(parts[2])
            if chrom not in genome:
                continue
            region = genome[chrom][start:end]
            # Center-crop or skip
            if len(region) < sequence_length:
                continue
            if len(region) > sequence_length:
                offset = (len(region) - sequence_length) // 2
                region = region[offset : offset + sequence_length]
            if _is_acgt_only(region):
                sequences.append(region)

    if len(sequences) == 0:
        raise RuntimeError(
            f"No valid {sequence_length}bp ACGT-only sequences found from "
            f"{bed_path} + {fasta_path}"
        )

    logger.info(
        "Extracted %d valid %dbp sequences from BED regions",
        len(sequences), sequence_length,
    )

    rng = random.Random(seed)
    if len(sequences) <= num_sequences:
        rng.shuffle(sequences)
        return sequences

    return rng.sample(sequences, num_sequences)


def _save_sequences_fasta(
    sequences: List[str],
    dataset_name: str,
    subset: Optional[str],
    output_dir: str,
) -> str:
    """Save extracted sequences as a FASTA file for local reproducibility."""
    os.makedirs(output_dir, exist_ok=True)
    safe_name = dataset_name.replace("/", "_")
    if subset:
        safe_name += f"_{subset}"
    fasta_path = os.path.join(output_dir, f"{safe_name}.fasta")
    with open(fasta_path, "w") as fh:
        for i, seq in enumerate(sequences):
            fh.write(f">seq_{i}\n{seq}\n")
    logger.info("Saved %d sequences to %s", len(sequences), fasta_path)
    return fasta_path


# ------------------------------------------------------------------
# Unified interface
# ------------------------------------------------------------------

def load_real_sequences(config: dict) -> Tuple[List[str], List[str]]:
    """Load real genomic train/test sequences based on config.

    Dispatches to the appropriate source loader based on
    ``config['data']['real_data']['source']``.

    Returns:
        ``(train_sequences, test_sequences)`` — both ``List[str]`` of
        ACGT-only strings.
    """
    data_config = config.get("data", {})
    real_cfg = data_config.get("real_data", {})
    source = real_cfg.get("source", "refseq")
    seed = config.get("experiment", {}).get("seed", 42)
    seq_len = data_config.get("sequence_length", 256)
    num_train = data_config.get("num_train_sequences", 1000)
    num_test = data_config.get("num_test_sequences", 200)
    total = num_train + num_test

    if source == "refseq":
        fasta_path = real_cfg.get("fasta_path")
        if fasta_path is None:
            accession = real_cfg.get("accession", "GCF_000005845.2")
            genome_dir = real_cfg.get("genome_dir", "data/genomes")
            fasta_path = download_reference_genome(accession, genome_dir)

        stride = real_cfg.get("stride", seq_len)
        all_seqs = load_from_fasta(
            fasta_path=fasta_path,
            num_sequences=total,
            sequence_length=seq_len,
            stride=stride,
            seed=seed,
        )

    elif source == "huggingface":
        hf_dataset = real_cfg.get("hf_dataset", "leannmlindsey/GUE")
        hf_subset = real_cfg.get("hf_subset")
        all_seqs = load_from_huggingface(
            dataset_name=hf_dataset,
            subset=hf_subset,
            split=real_cfg.get("hf_split", "train"),
            num_sequences=total,
            sequence_length=seq_len,
            seed=seed,
        )

        # Save extracted sequences locally for reproducibility
        hf_dir = real_cfg.get("hf_cache_dir", "data/huggingface")
        _save_sequences_fasta(all_seqs, hf_dataset, hf_subset, hf_dir)

    elif source == "bed":
        bed_path = real_cfg.get("bed_path")
        fasta_path = real_cfg.get("fasta_path")
        if bed_path is None or fasta_path is None:
            raise ValueError(
                "Both 'bed_path' and 'fasta_path' must be set for source='bed'"
            )
        all_seqs = load_from_bed(
            bed_path=bed_path,
            fasta_path=fasta_path,
            num_sequences=total,
            sequence_length=seq_len,
            seed=seed,
        )

    else:
        raise ValueError(f"Unknown real data source: '{source}'")

    # Train / test split
    rng = random.Random(seed)
    rng.shuffle(all_seqs)
    train_sequences = all_seqs[:num_train]
    test_sequences = all_seqs[num_train : num_train + num_test]

    logger.info(
        "Real data loaded: %d train, %d test sequences (%dbp, source=%s)",
        len(train_sequences), len(test_sequences), seq_len, source,
    )

    return train_sequences, test_sequences
