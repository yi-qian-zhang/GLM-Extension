"""
Genomic Dataset for PLM Training

PyTorch dataset classes for loading and processing DNA sequences
with support for canary insertion and train/test splitting.
Supports both the built-in DNATokenizer and HuggingFace tokenizers (e.g. DNABERT-2).
"""

import torch
from torch.utils.data import Dataset, DataLoader
from typing import Dict, List, Optional, Tuple, Any, Union
import numpy as np
from pathlib import Path

from .synthetic_generator import SyntheticDNAGenerator
from .canary_manager import CanaryManager


def is_hf_tokenizer(tokenizer: Any) -> bool:
    """Return True if tokenizer is a HuggingFace PreTrainedTokenizer-style object."""
    return (
        hasattr(tokenizer, "pad_token_id")
        and hasattr(tokenizer, "__call__")
        and hasattr(tokenizer, "model_max_length")
    )


def is_evo_tokenizer(tokenizer: Any) -> bool:
    """Return True if tokenizer is an EVO tokenizer (has tokenize() method returning token IDs)."""
    return (
        hasattr(tokenizer, "tokenize")
        and callable(tokenizer.tokenize)
        and not is_hf_tokenizer(tokenizer)
    )


def encode_sequence(
    tokenizer: Any,
    sequence: str,
    max_length: int,
    return_tensors: bool = True,
) -> Dict[str, Any]:
    """
    Encode a DNA sequence with DNATokenizer, HuggingFace tokenizer, or EVO tokenizer.
    Returns dict with input_ids and attention_mask (tensors if return_tensors=True).
    EVO uses left padding (pad_token_id=1); HF uses right padding.
    """
    # 1) HuggingFace tokenizer (HF has .encode and .vocab; HF expects return_tensors='pt' not True)
    if is_hf_tokenizer(tokenizer):
        enc = tokenizer(
            sequence,
            return_tensors="pt" if return_tensors else None,
            max_length=max_length,
            padding="max_length",
            truncation=True,
            add_special_tokens=True,
        )
        input_ids = enc["input_ids"]
        if "attention_mask" in enc:
            attention_mask = enc["attention_mask"]
        else:
            if return_tensors:
                attention_mask = torch.ones_like(input_ids, dtype=torch.long)
            else:
                attention_mask = [1] * len(input_ids)
        if return_tensors:
            if not isinstance(input_ids, torch.Tensor):
                input_ids = torch.tensor(input_ids, dtype=torch.long)
                attention_mask = torch.tensor(attention_mask, dtype=torch.long)
            if input_ids.dim() == 2:
                input_ids = input_ids.squeeze(0)
                attention_mask = attention_mask.squeeze(0)
        return {"input_ids": input_ids, "attention_mask": attention_mask}
    
    # 2) DNATokenizer (simple model): has .vocab and .encode; .tokenize() returns *strings*, not IDs
    #    Must be before EVO, since EVO also has .tokenize() but returns IDs.
    if hasattr(tokenizer, 'vocab') and hasattr(tokenizer, 'encode'):
        return tokenizer.encode(
            sequence,
            add_special_tokens=True,
            padding=True,
            truncation=True,
            return_tensors=return_tensors,
        )
    
    # 3) EVO tokenizer: tokenize() returns token IDs directly, uses LEFT padding (pad_id=1)
    if is_evo_tokenizer(tokenizer):
        token_ids = tokenizer.tokenize(sequence)
        if len(token_ids) > max_length:
            token_ids = token_ids[:max_length]
        pad_token_id = getattr(tokenizer, "pad_token_id", 1)
        if len(token_ids) < max_length:
            padding = [pad_token_id] * (max_length - len(token_ids))
            token_ids = padding + token_ids
        attention_mask = [0 if tid == pad_token_id else 1 for tid in token_ids]
        if return_tensors:
            input_ids = torch.tensor(token_ids, dtype=torch.long)
            attention_mask = torch.tensor(attention_mask, dtype=torch.long)
            return {"input_ids": input_ids, "attention_mask": attention_mask}
        return {"input_ids": token_ids, "attention_mask": attention_mask}
    
    raise ValueError(f"Unknown tokenizer type: {type(tokenizer)}. Expected DNATokenizer, HuggingFace tokenizer, or EVO tokenizer.")


def get_tokenizer_vocab_size(tokenizer: Any) -> int:
    """Return vocab size for DNATokenizer, HuggingFace tokenizer, or EVO tokenizer."""
    if is_hf_tokenizer(tokenizer):
        return len(tokenizer)
    if hasattr(tokenizer, 'vocab') and hasattr(tokenizer, 'encode'):
        return tokenizer.vocab_size
    if is_evo_tokenizer(tokenizer):
        if hasattr(tokenizer, "__len__"):
            return len(tokenizer)
        if hasattr(tokenizer, "vocab_size"):
            return tokenizer.vocab_size
        return 1000  # Common EVO vocab size
    return tokenizer.vocab_size


def get_tokenizer_for_model(config: Dict[str, Any]):
    """
    Create the appropriate tokenizer for the configured model.
    Returns DNATokenizer for 'simple', or HuggingFace AutoTokenizer for any
    HuggingFace genomic model (DNABERT-2, HyenaDNA, etc.).
    Used so dataloaders and model share the same tokenizer.
    """
    model_config = config.get("model", {})
    model_name = model_config.get("name", "simple")
    max_length = model_config.get("max_length", 512)
    
    if model_name == "simple":
        return DNATokenizer(max_length=max_length)
    
    # EVO model: load via Evo() class (Genome_Factory pattern)
    if "evo" in model_name.lower() and not model_name.lower().startswith("evol"):
        try:
            from evo import Evo
            evo_model = Evo(model_name)
            return evo_model.tokenizer
        except ImportError:
            raise RuntimeError(
                f"EVO package not installed. Install it with:\n"
                "  git clone https://github.com/evo-design/evo.git\n"
                "  cd evo\n"
                "  pip install .\n"
                "Then return to your project directory."
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to load EVO model/tokenizer for {model_name}. "
                "Ensure the model name is correct (e.g. 'evo-1-131k-base', 'evo-1-8k-base')."
            ) from e

    # HuggingFace genomic model (DNABERT-2, HyenaDNA, etc.)
    try:
        from transformers import AutoTokenizer
        return AutoTokenizer.from_pretrained(
            model_name,
            model_max_length=max_length,
            padding_side="right",
            use_fast=True,
            trust_remote_code=True,
        )
    except Exception as e:
        raise RuntimeError(
            f"Failed to load HuggingFace tokenizer for {model_name}. "
            "Install transformers and ensure the model ID is correct."
        ) from e


class DNATokenizer:
    """Simple tokenizer for DNA sequences."""
    
    def __init__(self, max_length: int = 512, kmer_size: int = 1):
        """
        Initialize the tokenizer.
        
        Args:
            max_length: Maximum sequence length
            kmer_size: Size of k-mers (1 for single nucleotides)
        """
        self.max_length = max_length
        self.kmer_size = kmer_size
        
        # Build vocabulary
        if kmer_size == 1:
            self.vocab = {'[PAD]': 0, '[UNK]': 1, '[CLS]': 2, '[SEP]': 3, 
                         'A': 4, 'C': 5, 'G': 6, 'T': 7}
        else:
            self.vocab = self._build_kmer_vocab()
        
        self.id_to_token = {v: k for k, v in self.vocab.items()}
        self.pad_token_id = self.vocab['[PAD]']
        self.unk_token_id = self.vocab['[UNK]']
        self.cls_token_id = self.vocab['[CLS]']
        self.sep_token_id = self.vocab['[SEP]']
        
    def _build_kmer_vocab(self) -> Dict[str, int]:
        """Build vocabulary for k-mers."""
        vocab = {'[PAD]': 0, '[UNK]': 1, '[CLS]': 2, '[SEP]': 3}
        nucleotides = ['A', 'C', 'G', 'T']
        
        def generate_kmers(k, prefix=''):
            if k == 0:
                return [prefix]
            kmers = []
            for nuc in nucleotides:
                kmers.extend(generate_kmers(k - 1, prefix + nuc))
            return kmers
        
        for idx, kmer in enumerate(generate_kmers(self.kmer_size)):
            vocab[kmer] = idx + 4
            
        return vocab
    
    def tokenize(self, sequence: str) -> List[str]:
        """Tokenize a DNA sequence into k-mers."""
        if self.kmer_size == 1:
            return list(sequence)
        
        tokens = []
        for i in range(0, len(sequence) - self.kmer_size + 1):
            tokens.append(sequence[i:i + self.kmer_size])
        return tokens
    
    def encode(
        self, 
        sequence: str,
        add_special_tokens: bool = True,
        padding: bool = True,
        truncation: bool = True,
        return_tensors: bool = True
    ) -> Dict[str, Any]:
        """
        Encode a DNA sequence.
        
        Args:
            sequence: DNA sequence string
            add_special_tokens: Add [CLS] and [SEP]
            padding: Pad to max_length
            truncation: Truncate to max_length
            return_tensors: Return as PyTorch tensors
            
        Returns:
            Dictionary with input_ids, attention_mask
        """
        tokens = self.tokenize(sequence)
        
        # Convert to IDs
        token_ids = [
            self.vocab.get(t, self.unk_token_id) 
            for t in tokens
        ]
        
        # Add special tokens
        if add_special_tokens:
            token_ids = [self.cls_token_id] + token_ids + [self.sep_token_id]
        
        # Truncation
        if truncation and len(token_ids) > self.max_length:
            token_ids = token_ids[:self.max_length]
        
        # Create attention mask
        attention_mask = [1] * len(token_ids)
        
        # Padding
        if padding and len(token_ids) < self.max_length:
            pad_length = self.max_length - len(token_ids)
            token_ids = token_ids + [self.pad_token_id] * pad_length
            attention_mask = attention_mask + [0] * pad_length
        
        result = {
            'input_ids': token_ids,
            'attention_mask': attention_mask
        }
        
        if return_tensors:
            result = {
                k: torch.tensor(v, dtype=torch.long) 
                for k, v in result.items()
            }
        
        return result
    
    def decode(self, token_ids: List[int]) -> str:
        """Decode token IDs back to sequence."""
        tokens = [
            self.id_to_token.get(tid, '[UNK]') 
            for tid in token_ids
            if tid not in [self.pad_token_id, self.cls_token_id, self.sep_token_id]
        ]
        return ''.join(tokens)
    
    @property
    def vocab_size(self) -> int:
        return len(self.vocab)


class GenomicDataset(Dataset):
    """PyTorch Dataset for genomic sequences. Supports DNATokenizer and HuggingFace tokenizers."""
    
    def __init__(
        self,
        sequences: List[str],
        tokenizer: Union[DNATokenizer, Any],
        is_canary: Optional[List[bool]] = None,
        canary_ids: Optional[List[Optional[str]]] = None,
        max_length: Optional[int] = None,
    ):
        """
        Initialize the dataset.
        
        Args:
            sequences: List of DNA sequences
            tokenizer: Tokenizer (DNATokenizer or HuggingFace PreTrainedTokenizer)
            is_canary: Boolean mask indicating canary sequences
            canary_ids: Canary IDs for each sequence (None if not canary)
            max_length: Max sequence length (required for HF tokenizer; for DNATokenizer uses tokenizer.max_length)
        """
        self.sequences = sequences
        self.tokenizer = tokenizer
        self.is_canary = is_canary or [False] * len(sequences)
        self.canary_ids = canary_ids or [None] * len(sequences)
        if max_length is not None:
            self.max_length = max_length
        elif is_hf_tokenizer(tokenizer):
            self.max_length = getattr(tokenizer, "model_max_length", 512)
        else:
            self.max_length = getattr(tokenizer, "max_length", 512)
        
    def __len__(self) -> int:
        return len(self.sequences)
    
    def __getitem__(self, idx: int) -> Dict[str, Any]:
        sequence = self.sequences[idx]
        encoded = encode_sequence(
            self.tokenizer,
            sequence,
            self.max_length,
            return_tensors=True,
        )
        labels = encoded["input_ids"].clone()
        
        return {
            "input_ids": encoded["input_ids"],
            "attention_mask": encoded["attention_mask"],
            "labels": labels,
            "is_canary": self.is_canary[idx],
            "canary_id": self.canary_ids[idx],
            "sequence": sequence,
            "idx": idx,
        }
    
    def get_canary_indices(self) -> List[int]:
        """Get indices of all canary sequences."""
        return [i for i, is_c in enumerate(self.is_canary) if is_c]
    
    def get_non_canary_indices(self) -> List[int]:
        """Get indices of all non-canary sequences."""
        return [i for i, is_c in enumerate(self.is_canary) if not is_c]


def create_dataloaders(
    config: Dict[str, Any],
    tokenizer: Optional[Union[DNATokenizer, Any]] = None,
) -> Tuple[DataLoader, DataLoader, CanaryManager, Dict[str, Any]]:
    """
    Create train and test dataloaders with canaries.
    
    Supports data.mode: "synthetic" | "real" | "refseq" | "huggingface" | "mixed".
    For real/refseq/huggingface/mixed, uses data.real_data and real_data_loader.
    
    Args:
        config: Configuration dictionary
        tokenizer: Optional tokenizer (created if not provided; DNATokenizer or HuggingFace)
        
    Returns:
        Tuple of (train_loader, test_loader, canary_manager, metadata)
    """
    data_config = config.get("data", {})
    model_config = config.get("model", {})
    max_length = model_config.get("max_length", 512)
    
    # Initialize tokenizer if not provided
    if tokenizer is None:
        tokenizer = DNATokenizer(max_length=max_length)
    
    # Generate or load sequences based on data.mode
    data_mode = data_config.get("mode", "synthetic")
    
    if data_mode == "synthetic":
        generator = SyntheticDNAGenerator(seed=config.get('experiment', {}).get('seed', 42))
        train_sequences = generator.generate_sequences(
            num_sequences=data_config.get('num_train_sequences', 1000),
            length=data_config.get('sequence_length', 256),
            gc_content=data_config.get('gc_content', 0.5)
        )
        test_sequences = generator.generate_sequences(
            num_sequences=data_config.get('num_test_sequences', 200),
            length=data_config.get('sequence_length', 256),
            gc_content=data_config.get('gc_content', 0.5)
        )
    elif data_mode in ("refseq", "real", "huggingface"):
        from .real_data_loader import load_real_sequences
        train_sequences, test_sequences = load_real_sequences(config)
    elif data_mode == "mixed":
        from .real_data_loader import load_real_sequences
        seed = config.get("experiment", {}).get("seed", 42)
        num_train = data_config.get("num_train_sequences", 1000)
        num_test = data_config.get("num_test_sequences", 200)
        half_train = num_train // 2
        half_test = num_test // 2
        mixed_data = {
            **data_config,
            "num_train_sequences": half_train,
            "num_test_sequences": half_test,
        }
        mixed_config = {**config, "data": mixed_data}
        real_train, real_test = load_real_sequences(mixed_config)
        generator = SyntheticDNAGenerator(seed=seed)
        syn_train = generator.generate_sequences(
            num_sequences=num_train - half_train,
            length=data_config.get("sequence_length", 256),
            gc_content=data_config.get("gc_content", 0.5),
        )
        syn_test = generator.generate_sequences(
            num_sequences=num_test - half_test,
            length=data_config.get("sequence_length", 256),
            gc_content=data_config.get("gc_content", 0.5),
        )
        import random as _random
        rng = _random.Random(seed)
        train_sequences = real_train + syn_train
        rng.shuffle(train_sequences)
        test_sequences = real_test + syn_test
        rng.shuffle(test_sequences)
    else:
        raise ValueError(f"Unknown data mode: '{data_mode}'")
    
    # Set up canary manager
    canary_config = data_config.get('canaries', {})
    canary_manager = None
    is_canary_train = [False] * len(train_sequences)
    canary_ids_train = [None] * len(train_sequences)
    
    if canary_config.get('enabled', True):
        canary_manager = CanaryManager(
            num_canaries=canary_config.get('num_canaries', 50),
            canary_length=canary_config.get('canary_length', 64),
            repetitions=canary_config.get('repetitions', [1, 5, 10, 20]),
            seed=config.get('experiment', {}).get('seed', 42) + 1000,
            marker_pattern=None  # Don't use text patterns in DNA
        )
        
        # Insert canaries into training data
        train_sequences, insertion_map = canary_manager.insert_canaries(train_sequences)
        
        # Update canary tracking
        is_canary_train = [False] * len(train_sequences)
        canary_ids_train = [None] * len(train_sequences)
        
        for canary_id, canary in canary_manager.canaries.items():
            for pos in canary.insertion_positions:
                if pos < len(is_canary_train):
                    is_canary_train[pos] = True
                    canary_ids_train[pos] = canary_id
    
    # Create datasets (pass max_length for HF tokenizers)
    train_dataset = GenomicDataset(
        sequences=train_sequences,
        tokenizer=tokenizer,
        is_canary=is_canary_train,
        canary_ids=canary_ids_train,
        max_length=max_length,
    )
    
    test_dataset = GenomicDataset(
        sequences=test_sequences,
        tokenizer=tokenizer,
        max_length=max_length,
    )
    
    # Create dataloaders (support train_batch_size / eval_batch_size with fallback to batch_size)
    train_cfg = config.get("training", {})
    train_batch_size = train_cfg.get("train_batch_size", train_cfg.get("batch_size", 16))
    eval_batch_size = train_cfg.get("eval_batch_size", train_cfg.get("batch_size", 16))
    train_loader = DataLoader(
        train_dataset,
        batch_size=train_batch_size,
        shuffle=True,
        num_workers=0,
        collate_fn=collate_genomic_batch
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=eval_batch_size,
        shuffle=False,
        num_workers=0,
        collate_fn=collate_genomic_batch
    )
    
    metadata = {
        "num_train_sequences": len(train_sequences),
        "num_test_sequences": len(test_sequences),
        "num_canaries": len(canary_manager.canaries) if canary_manager else 0,
        "vocab_size": get_tokenizer_vocab_size(tokenizer),
        "tokenizer": tokenizer,
    }
    
    return train_loader, test_loader, canary_manager, metadata


def collate_genomic_batch(batch: List[Dict]) -> Dict[str, Any]:
    """Custom collate function for genomic batches."""
    return {
        'input_ids': torch.stack([item['input_ids'] for item in batch]),
        'attention_mask': torch.stack([item['attention_mask'] for item in batch]),
        'labels': torch.stack([item['labels'] for item in batch]),
        'is_canary': [item['is_canary'] for item in batch],
        'canary_id': [item['canary_id'] for item in batch],
        'sequences': [item['sequence'] for item in batch],
        'indices': [item['idx'] for item in batch]
    }
