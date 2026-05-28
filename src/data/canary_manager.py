"""
Canary Manager for Memorization Experiments

Manages the insertion, tracking, and evaluation of canary sequences
used to measure memorization in trained models.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path

from .synthetic_generator import SyntheticDNAGenerator


@dataclass
class Canary:
    """Represents a canary sequence for memorization testing."""
    sequence: str
    canary_id: str
    repetitions: int
    length: int
    insertion_positions: List[int] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'sequence': self.sequence,
            'canary_id': self.canary_id,
            'repetitions': self.repetitions,
            'length': self.length,
            'insertion_positions': self.insertion_positions,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Canary':
        return cls(**data)


class CanaryManager:
    """
    Manages canary sequences for memorization experiments.
    
    Canaries are unique sequences inserted into training data at known
    positions and repetitions to measure how much a model memorizes.
    """
    
    def __init__(
        self,
        num_canaries: int,
        canary_length: int,
        repetitions: List[int],
        seed: Optional[int] = None,
        marker_pattern: Optional[str] = None
    ):
        """
        Initialize the canary manager.
        
        Args:
            num_canaries: Number of canary sequences to generate
            canary_length: Length of each canary sequence
            repetitions: List of repetition counts for different canaries
            seed: Random seed for reproducibility
            marker_pattern: Optional pattern to include in canaries
        """
        self.num_canaries = num_canaries
        self.canary_length = canary_length
        self.repetitions = repetitions
        self.seed = seed
        self.marker_pattern = marker_pattern
        
        self.generator = SyntheticDNAGenerator(seed)
        self.rng = np.random.default_rng(seed)
        
        self.canaries: Dict[str, Canary] = {}
        self._generate_canaries()
    
    def _generate_canary_id(self, sequence: str, idx: int) -> str:
        """Generate a unique ID for a canary."""
        hash_input = f"{sequence}_{idx}_{self.seed}"
        return f"canary_{hashlib.sha256(hash_input.encode()).hexdigest()[:8]}"
    
    def _generate_canaries(self) -> None:
        """Generate all canary sequences."""
        # Distribute repetitions across canaries
        canaries_per_rep = self.num_canaries // len(self.repetitions)
        remainder = self.num_canaries % len(self.repetitions)
        
        canary_idx = 0
        
        for rep_idx, rep_count in enumerate(self.repetitions):
            # Calculate how many canaries get this repetition count
            count = canaries_per_rep + (1 if rep_idx < remainder else 0)
            
            for _ in range(count):
                # Generate unique canary sequence
                if self.marker_pattern:
                    # Embed marker pattern in canary
                    seq, _ = self.generator.generate_with_pattern(
                        self.canary_length,
                        self.marker_pattern,
                        gc_content=0.5
                    )
                else:
                    seq = self.generator.generate_sequence(
                        self.canary_length,
                        gc_content=0.5
                    )
                
                canary_id = self._generate_canary_id(seq, canary_idx)
                
                # Ensure uniqueness
                while canary_id in self.canaries or any(
                    c.sequence == seq for c in self.canaries.values()
                ):
                    seq = self.generator.generate_sequence(
                        self.canary_length,
                        gc_content=0.5
                    )
                    canary_id = self._generate_canary_id(seq, canary_idx)
                
                canary = Canary(
                    sequence=seq,
                    canary_id=canary_id,
                    repetitions=rep_count,
                    length=self.canary_length,
                    metadata={'repetition_group': rep_idx}
                )
                
                self.canaries[canary_id] = canary
                canary_idx += 1
    
    def insert_canaries(
        self,
        sequences: List[str]
    ) -> Tuple[List[str], Dict[str, List[int]]]:
        """
        Insert canaries into a list of sequences.
        
        Args:
            sequences: List of sequences to extend with canaries
            
        Returns:
            Tuple of (extended_sequences, insertion_map)
            insertion_map maps canary_id -> list of positions in extended_sequences
        """
        extended = list(sequences)
        insertion_map = {}
        
        for canary_id, canary in self.canaries.items():
            positions = []
            
            for _ in range(canary.repetitions):
                # Insert at random position
                pos = int(self.rng.integers(0, len(extended) + 1))
                extended.insert(pos, canary.sequence)
                
                # Track position (note: positions shift as we insert)
                positions.append(pos)
            
            canary.insertion_positions = sorted(positions)
            insertion_map[canary_id] = positions
        
        return extended, insertion_map
    
    def get_canary_sequences(self) -> List[str]:
        """Get all canary sequences."""
        return [c.sequence for c in self.canaries.values()]
    
    def get_canaries_by_repetition(self, repetitions: int) -> List[Canary]:
        """Get all canaries with a specific repetition count."""
        return [c for c in self.canaries.values() if c.repetitions == repetitions]
    
    def is_canary(self, sequence: str) -> Optional[str]:
        """Check if a sequence is a canary. Returns canary_id if found."""
        for canary_id, canary in self.canaries.items():
            if canary.sequence == sequence:
                return canary_id
        return None
    
    def compute_exposure(
        self,
        canary_id: str,
        rank: int,
        vocab_size: int = 4,  # A, C, G, T
    ) -> float:
        """
        Compute the exposure metric for a canary.
        
        Exposure = log2(|candidate_set|) - log2(rank)
        
        Higher exposure means more memorization.
        
        Args:
            canary_id: ID of the canary
            rank: Rank of true canary among candidates
            vocab_size: Size of vocabulary
            
        Returns:
            Exposure score
        """
        canary = self.canaries.get(canary_id)
        if canary is None:
            raise ValueError(f"Unknown canary: {canary_id}")
        
        # Candidate set size = vocab^length
        candidate_set_size = vocab_size ** canary.length
        
        if rank <= 0:
            return float('inf')
        
        exposure = np.log2(float(candidate_set_size)) - np.log2(float(rank))
        
        return exposure
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the canaries."""
        repetition_counts = {}
        for canary in self.canaries.values():
            rep = canary.repetitions
            repetition_counts[rep] = repetition_counts.get(rep, 0) + 1
        
        return {
            'total_canaries': len(self.canaries),
            'canary_length': self.canary_length,
            'repetition_distribution': repetition_counts,
            'total_insertions': sum(c.repetitions for c in self.canaries.values()),
            'has_marker': self.marker_pattern is not None
        }
    
    def save(self, path: str) -> None:
        """Save canary configuration to file."""
        data = {
            'config': {
                'num_canaries': self.num_canaries,
                'canary_length': self.canary_length,
                'repetitions': self.repetitions,
                'seed': self.seed,
                'marker_pattern': self.marker_pattern
            },
            'canaries': {
                cid: c.to_dict() for cid, c in self.canaries.items()
            }
        }
        
        Path(path).write_text(json.dumps(data, indent=2))
    
    @classmethod
    def load(cls, path: str) -> 'CanaryManager':
        """Load canary configuration from file."""
        data = json.loads(Path(path).read_text())
        
        manager = cls(
            num_canaries=data['config']['num_canaries'],
            canary_length=data['config']['canary_length'],
            repetitions=data['config']['repetitions'],
            seed=data['config']['seed'],
            marker_pattern=data['config']['marker_pattern']
        )
        
        # Override generated canaries with saved ones
        manager.canaries = {
            cid: Canary.from_dict(cdata) 
            for cid, cdata in data['canaries'].items()
        }
        
        return manager
