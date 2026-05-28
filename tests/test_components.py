"""
Unit tests for the PLM Memorization Experiment
"""

import pytest
import numpy as np
import torch
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.synthetic_generator import SyntheticDNAGenerator
from src.data.canary_manager import CanaryManager
from src.data.dataset import DNATokenizer, GenomicDataset
from src.models.dnabert_wrapper import DNABERTWrapper, SimpleDNALM


class TestSyntheticDNAGenerator:
    """Tests for DNA sequence generator."""
    
    def test_generate_sequence_valid_nucleotides(self):
        """Generated sequences contain only valid nucleotides."""
        generator = SyntheticDNAGenerator(seed=42)
        sequence = generator.generate_sequence(100)
        
        assert len(sequence) == 100
        assert all(nuc in 'ACGT' for nuc in sequence)
    
    def test_generate_sequence_gc_content(self):
        """GC content is approximately correct."""
        generator = SyntheticDNAGenerator(seed=42)
        
        # High GC content
        seq_high = generator.generate_sequence(1000, gc_content=0.8)
        gc_high = generator.compute_gc_content(seq_high)
        assert 0.7 < gc_high < 0.9
        
        # Low GC content
        seq_low = generator.generate_sequence(1000, gc_content=0.2)
        gc_low = generator.compute_gc_content(seq_low)
        assert 0.1 < gc_low < 0.3
    
    def test_generate_sequences_unique(self):
        """Generated sequences are unique."""
        generator = SyntheticDNAGenerator(seed=42)
        sequences = generator.generate_sequences(100, length=50, unique=True)
        
        assert len(sequences) == 100
        assert len(set(sequences)) == 100  # All unique
    
    def test_reproducibility(self):
        """Same seed produces same sequences."""
        gen1 = SyntheticDNAGenerator(seed=42)
        gen2 = SyntheticDNAGenerator(seed=42)
        
        seq1 = gen1.generate_sequence(100)
        seq2 = gen2.generate_sequence(100)
        
        assert seq1 == seq2
    
    def test_generate_with_pattern(self):
        """Pattern is correctly embedded."""
        generator = SyntheticDNAGenerator(seed=42)
        pattern = "ACGTACGT"
        seq, pos = generator.generate_with_pattern(50, pattern)
        
        assert len(seq) == 50
        assert pattern in seq
        assert seq[pos:pos+len(pattern)] == pattern


class TestCanaryManager:
    """Tests for canary management."""
    
    def test_canary_generation(self):
        """Correct number of canaries are generated."""
        manager = CanaryManager(
            num_canaries=20,
            canary_length=32,
            repetitions=[1, 5, 10],
            seed=42
        )
        
        assert len(manager.canaries) == 20
    
    def test_canary_uniqueness(self):
        """All canaries are unique."""
        manager = CanaryManager(
            num_canaries=50,
            canary_length=32,
            repetitions=[1, 5],
            seed=42
        )
        
        sequences = manager.get_canary_sequences()
        assert len(set(sequences)) == len(sequences)
    
    def test_canary_insertion(self):
        """Canaries are inserted into sequences."""
        manager = CanaryManager(
            num_canaries=5,
            canary_length=16,
            repetitions=[2],
            seed=42
        )
        
        original_seqs = ["ACGT" * 10] * 20
        extended, insertion_map = manager.insert_canaries(original_seqs)
        
        # Should have more sequences after insertion
        expected_insertions = 5 * 2  # 5 canaries, 2 repetitions each
        assert len(extended) == len(original_seqs) + expected_insertions
    
    def test_exposure_computation(self):
        """Exposure score is computed correctly."""
        manager = CanaryManager(
            num_canaries=1,
            canary_length=8,
            repetitions=[1],
            seed=42
        )
        
        canary_id = list(manager.canaries.keys())[0]
        
        # Rank 1 should give maximum exposure
        exposure_rank1 = manager.compute_exposure(canary_id, rank=1, vocab_size=4)
        # 4^8 = 65536 candidates, log2(65536) = 16
        assert exposure_rank1 == 16.0
        
        # Higher rank = lower exposure
        exposure_rank10 = manager.compute_exposure(canary_id, rank=10, vocab_size=4)
        assert exposure_rank10 < exposure_rank1


class TestDNATokenizer:
    """Tests for DNA tokenizer."""
    
    def test_tokenize(self):
        """Tokenization produces correct tokens."""
        tokenizer = DNATokenizer(max_length=20)
        tokens = tokenizer.tokenize("ACGT")
        
        assert tokens == ['A', 'C', 'G', 'T']
    
    def test_encode_decode(self):
        """Encoding and decoding are reversible."""
        tokenizer = DNATokenizer(max_length=50)
        sequence = "ACGTACGTACGT"
        
        encoded = tokenizer.encode(sequence, return_tensors=False)
        decoded = tokenizer.decode(encoded['input_ids'])
        
        assert decoded == sequence
    
    def test_padding(self):
        """Sequences are padded correctly."""
        tokenizer = DNATokenizer(max_length=20)
        encoded = tokenizer.encode("ACGT")
        
        assert len(encoded['input_ids']) == 20
        assert encoded['attention_mask'].sum() == 6  # CLS + 4 + SEP
    
    def test_truncation(self):
        """Long sequences are truncated."""
        tokenizer = DNATokenizer(max_length=10)
        long_seq = "A" * 100
        
        encoded = tokenizer.encode(long_seq)
        assert len(encoded['input_ids']) == 10


class TestSimpleDNALM:
    """Tests for the simple DNA language model."""
    
    def test_forward_pass(self):
        """Forward pass produces correct output shapes."""
        model = SimpleDNALM(
            vocab_size=8,
            hidden_size=64,
            num_layers=2,
            num_heads=2,
            max_length=32
        )
        
        batch_size = 4
        seq_len = 16
        input_ids = torch.randint(0, 8, (batch_size, seq_len))
        
        outputs = model(input_ids)
        
        assert 'logits' in outputs
        assert outputs['logits'].shape == (batch_size, seq_len, 8)
    
    def test_loss_computation(self):
        """Loss is computed when labels provided."""
        model = SimpleDNALM(vocab_size=8, hidden_size=64, num_layers=2)
        
        input_ids = torch.randint(0, 8, (2, 10))
        outputs = model(input_ids, labels=input_ids)
        
        assert 'loss' in outputs
        assert outputs['loss'] is not None
        assert outputs['loss'].ndim == 0  # Scalar


class TestDNABERTWrapper:
    """Tests for the model wrapper."""
    
    def test_perplexity_computation(self):
        """Perplexity is computed correctly."""
        wrapper = DNABERTWrapper(model_name="simple", max_length=32)
        
        input_ids = torch.randint(4, 8, (2, 16))  # Only nucleotide tokens
        perplexity = wrapper.compute_perplexity(input_ids)
        
        assert perplexity.shape == (2,)
        assert all(p > 0 for p in perplexity)
    
    def test_generation(self):
        """Model can generate sequences."""
        wrapper = DNABERTWrapper(model_name="simple", max_length=32)
        
        prefix = torch.tensor([[2, 4, 5, 6, 7]])  # CLS + ACGT
        generated = wrapper.generate(prefix, max_new_tokens=5)
        
        assert generated.shape[1] == prefix.shape[1] + 5


# Run tests
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
