"""
Synthetic DNA Sequence Generator

Generates random DNA sequences for safe memorization experiments.
Uses only A, C, G, T nucleotides with configurable GC content.
"""

import numpy as np
from typing import List, Optional, Tuple
import hashlib


class SyntheticDNAGenerator:
    """Generate synthetic DNA sequences for safe experimentation."""
    
    NUCLEOTIDES = ['A', 'C', 'G', 'T']
    GC_NUCLEOTIDES = ['G', 'C']
    AT_NUCLEOTIDES = ['A', 'T']
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize the generator.
        
        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        
    def generate_sequence(
        self, 
        length: int, 
        gc_content: float = 0.5
    ) -> str:
        """
        Generate a single DNA sequence.
        
        Args:
            length: Length of sequence to generate
            gc_content: Target GC content (0.0 to 1.0)
            
        Returns:
            DNA sequence string
        """
        if not 0.0 <= gc_content <= 1.0:
            raise ValueError("gc_content must be between 0.0 and 1.0")
            
        # Generate nucleotides with weighted probabilities
        gc_prob = gc_content / 2  # Split between G and C
        at_prob = (1 - gc_content) / 2  # Split between A and T
        
        weights = [at_prob, gc_prob, gc_prob, at_prob]  # A, C, G, T
        
        sequence = self.rng.choice(
            self.NUCLEOTIDES, 
            size=length, 
            p=weights
        )
        
        return ''.join(sequence)
    
    def generate_sequences(
        self,
        num_sequences: int,
        length: int,
        gc_content: float = 0.5,
        unique: bool = True
    ) -> List[str]:
        """
        Generate multiple DNA sequences.
        
        Args:
            num_sequences: Number of sequences to generate
            length: Length of each sequence
            gc_content: Target GC content
            unique: If True, ensure all sequences are unique
            
        Returns:
            List of DNA sequences
        """
        sequences = []
        seen = set()
        
        attempts = 0
        max_attempts = num_sequences * 10  # Prevent infinite loops
        
        while len(sequences) < num_sequences and attempts < max_attempts:
            seq = self.generate_sequence(length, gc_content)
            
            if unique:
                if seq not in seen:
                    seen.add(seq)
                    sequences.append(seq)
            else:
                sequences.append(seq)
                
            attempts += 1
            
        if len(sequences) < num_sequences:
            raise RuntimeError(
                f"Could only generate {len(sequences)} unique sequences "
                f"out of {num_sequences} requested"
            )
            
        return sequences
    
    def generate_with_pattern(
        self,
        length: int,
        pattern: str,
        position: Optional[int] = None,
        gc_content: float = 0.5
    ) -> Tuple[str, int]:
        """
        Generate a sequence containing a specific pattern.
        
        Args:
            length: Total length of sequence
            pattern: Pattern to embed
            position: Position to place pattern (random if None)
            gc_content: GC content for random parts
            
        Returns:
            Tuple of (sequence, pattern_position)
        """
        if len(pattern) > length:
            raise ValueError("Pattern longer than sequence length")
            
        # Validate pattern contains only valid nucleotides
        valid_chars = set(self.NUCLEOTIDES)
        for char in pattern:
            if char not in valid_chars:
                raise ValueError(f"Invalid nucleotide in pattern: {char}")
        
        if position is None:
            position = self.rng.integers(0, length - len(pattern) + 1)
        
        # Generate prefix and suffix
        prefix = self.generate_sequence(position, gc_content) if position > 0 else ""
        suffix_len = length - position - len(pattern)
        suffix = self.generate_sequence(suffix_len, gc_content) if suffix_len > 0 else ""
        
        sequence = prefix + pattern + suffix
        
        return sequence, position
    
    def compute_gc_content(self, sequence: str) -> float:
        """Compute actual GC content of a sequence."""
        if len(sequence) == 0:
            return 0.0
        gc_count = sum(1 for nuc in sequence if nuc in self.GC_NUCLEOTIDES)
        return gc_count / len(sequence)
    
    def sequence_hash(self, sequence: str) -> str:
        """Compute a hash of a sequence for tracking."""
        return hashlib.sha256(sequence.encode()).hexdigest()[:16]
    
    def verify_valid_sequence(self, sequence: str) -> bool:
        """Check if a sequence contains only valid nucleotides."""
        valid = set(self.NUCLEOTIDES)
        return all(nuc in valid for nuc in sequence)


def generate_diverse_dataset(
    num_sequences: int,
    length: int,
    gc_contents: Optional[List[float]] = None,
    seed: Optional[int] = None
) -> List[Tuple[str, float]]:
    """
    Generate a diverse dataset with varying GC contents.
    
    Args:
        num_sequences: Total number of sequences
        length: Length of each sequence
        gc_contents: List of GC contents to sample from
        seed: Random seed
        
    Returns:
        List of (sequence, gc_content) tuples
    """
    if gc_contents is None:
        gc_contents = [0.3, 0.4, 0.5, 0.6, 0.7]
    
    generator = SyntheticDNAGenerator(seed)
    rng = np.random.default_rng(seed)
    
    dataset = []
    for _ in range(num_sequences):
        gc = rng.choice(gc_contents)
        seq = generator.generate_sequence(length, gc)
        dataset.append((seq, gc))
    
    return dataset
