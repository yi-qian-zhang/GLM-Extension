"""
Canary Extraction Attack

Attempts to extract memorized canary sequences by
searching the model's output space.
"""

import torch
import torch.nn.functional as F
import numpy as np
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
import heapq

from ..models.dnabert_wrapper import DNABERTWrapper
from ..data.canary_manager import CanaryManager
from ..data.dataset import DNATokenizer, is_hf_tokenizer, is_evo_tokenizer, encode_sequence


@dataclass
class ExtractionResult:
    """Result of extraction attack on a canary."""
    canary_id: str
    true_sequence: str
    rank: int  # Rank of true sequence among candidates
    exposure: float  # Exposure score
    top_candidates: List[Tuple[str, float]]  # (sequence, log_prob) pairs
    success: bool  # Whether canary was in top-k


class ExtractionAttack:
    """
    Canary extraction attack.
    
    Uses beam search to find high-probability sequences and checks
    if planted canaries appear among the top candidates.
    """
    
    def __init__(
        self,
        model: DNABERTWrapper,
        tokenizer: Any,
        canary_manager: CanaryManager
    ):
        """
        Initialize the attack.
        
        Args:
            model: Trained model to attack
            tokenizer: Tokenizer (DNATokenizer or HuggingFace) for encoding/decoding
            canary_manager: Manager with canary information
        """
        self.model = model
        self.tokenizer = tokenizer
        self.canary_manager = canary_manager
        
        # Token IDs used for generation: single nucleotides for DNATokenizer,
        # all non-special tokens for HuggingFace (e.g. DNABERT-2 k-mers)
        self.nucleotide_ids = self._get_generation_token_ids()
    
    def _get_generation_token_ids(self) -> List[int]:
        """Return list of token IDs valid for next-token generation."""
        if is_evo_tokenizer(self.tokenizer):
            # EVO tokenizer: exclude pad_token_id (typically 1) and other special tokens
            special = set()
            pad_token_id = getattr(self.tokenizer, "pad_token_id", 1)
            if pad_token_id is not None:
                special.add(pad_token_id)
            # Get vocab size (try multiple methods)
            vocab_size = getattr(self.tokenizer, "__len__", None)
            if vocab_size is None:
                vocab_size = getattr(self.tokenizer, "vocab_size", 1000)
            if callable(vocab_size):
                vocab_size = vocab_size()
            return [i for i in range(vocab_size) if i not in special]
        elif is_hf_tokenizer(self.tokenizer):
            special = set()
            for name in ("pad_token_id", "unk_token_id", "cls_token_id", "sep_token_id", "mask_token_id"):
                tid = getattr(self.tokenizer, name, None)
                if tid is not None:
                    special.add(tid)
            return [i for i in range(len(self.tokenizer)) if i not in special]
        return [self.tokenizer.vocab[n] for n in ["A", "C", "G", "T"]]
        
    def beam_search_generate(
        self,
        prefix_ids: torch.Tensor,
        length: int,
        beam_width: int = 10
    ) -> List[Tuple[torch.Tensor, float]]:
        """
        Generate sequences using beam search.
        
        Args:
            prefix_ids: Starting token IDs [1, prefix_len]
            length: Number of tokens to generate
            beam_width: Number of beams to keep
            
        Returns:
            List of (sequence_ids, log_probability) tuples
        """
        self.model.eval_mode()
        device = self.model.device
        prefix_ids = prefix_ids.to(device)
        
        # Initialize beams: (log_prob, sequence_ids)
        beams = [(0.0, prefix_ids)]
        
        with torch.no_grad():
            for step in range(length):
                all_candidates = []
                
                for log_prob, seq in beams:
                    # Get next token probabilities
                    outputs = self.model.forward(seq)
                    next_logits = outputs['logits'][0, -1, :]
                    
                    # Only consider generation tokens (nucleotides or k-mers)
                    nucleotide_logits = next_logits[self.nucleotide_ids]
                    log_probs = F.log_softmax(nucleotide_logits, dim=-1)
                    # For large vocabs (e.g. DNABERT-2 k-mers), expand only top-k by prob
                    max_expand = min(64, len(self.nucleotide_ids))
                    if max_expand < len(self.nucleotide_ids):
                        top_probs, top_pos = log_probs.topk(max_expand, dim=-1)
                        expand_ids = [self.nucleotide_ids[i] for i in top_pos.tolist()]
                        expand_probs = top_probs.tolist()
                    else:
                        expand_ids = self.nucleotide_ids
                        expand_probs = log_probs.tolist()
                    for idx, token_id in enumerate(expand_ids):
                        new_log_prob = log_prob + expand_probs[idx]
                        new_seq = torch.cat([
                            seq,
                            torch.tensor([[token_id]], device=device)
                        ], dim=1)
                        all_candidates.append((new_log_prob, new_seq))
                
                # Keep top beam_width candidates
                all_candidates.sort(key=lambda x: -x[0])  # Sort by log_prob desc
                beams = all_candidates[:beam_width]
        
        return [(seq, log_prob) for log_prob, seq in beams]
    
    def compute_sequence_log_prob(
        self,
        sequence: str,
        prefix_length: int = 0
    ) -> float:
        """
        Compute the log probability of a sequence.
        
        Args:
            sequence: DNA sequence string
            prefix_length: Length of prefix to condition on
            
        Returns:
            Log probability of the sequence
        """
        self.model.eval_mode()
        
        max_length = getattr(self.model, "max_length", 512)
        encoded = encode_sequence(
            self.tokenizer, sequence, max_length, return_tensors=True
        )
        input_ids = encoded["input_ids"].unsqueeze(0).to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.forward(input_ids)
            logits = outputs['logits']
            
            # Get log probabilities
            log_probs = F.log_softmax(logits, dim=-1)
            
            # Compute sum of log probs for each token given previous tokens
            total_log_prob = 0.0
            start_idx = prefix_length + 1  # Skip prefix and [CLS]
            
            for i in range(start_idx, input_ids.size(1) - 1):
                next_token = input_ids[0, i + 1].item()
                total_log_prob += log_probs[0, i, next_token].item()
        
        return total_log_prob
    
    def rank_canary(
        self,
        canary_id: str,
        num_candidates: int = 1000
    ) -> Tuple[int, float]:
        """
        Compute the rank of a canary among random candidates.
        
        Args:
            canary_id: ID of the canary to rank
            num_candidates: Number of random candidates to generate
            
        Returns:
            Tuple of (rank, exposure_score)
        """
        canary = self.canary_manager.canaries[canary_id]
        canary_log_prob = self.compute_sequence_log_prob(canary.sequence)
        
        # Generate random candidates
        rng = np.random.default_rng(42)
        nucleotides = ['A', 'C', 'G', 'T']
        
        higher_count = 0
        for _ in range(num_candidates):
            random_seq = ''.join(
                rng.choice(nucleotides, size=canary.length)
            )
            random_log_prob = self.compute_sequence_log_prob(random_seq)
            
            if random_log_prob > canary_log_prob:
                higher_count += 1
        
        # Estimate rank
        rank = higher_count + 1
        
        # Compute exposure
        exposure = self.canary_manager.compute_exposure(
            canary_id, rank, vocab_size=4
        )
        
        return rank, exposure
    
    def attack_all_canaries(
        self,
        num_candidates: int = 1000,
        success_threshold: int = 100
    ) -> Dict[str, Any]:
        """
        Run extraction attack on all canaries.
        
        Args:
            num_candidates: Number of candidates for ranking
            success_threshold: Rank threshold for "successful" extraction
            
        Returns:
            Attack results dictionary
        """
        results = {}
        exposures_by_rep = defaultdict(list)
        
        for canary_id, canary in self.canary_manager.canaries.items():
            rank, exposure = self.rank_canary(canary_id, num_candidates)
            
            result = ExtractionResult(
                canary_id=canary_id,
                true_sequence=canary.sequence,
                rank=rank,
                exposure=exposure,
                top_candidates=[],  # Could populate with beam search
                success=rank <= success_threshold
            )
            
            results[canary_id] = result
            exposures_by_rep[canary.repetitions].append(exposure)
        
        # Compute summary statistics
        all_exposures = [r.exposure for r in results.values()]
        all_ranks = [r.rank for r in results.values()]
        success_count = sum(1 for r in results.values() if r.success)
        
        summary = {
            'num_canaries': len(results),
            'success_rate': success_count / len(results) if results else 0,
            'mean_exposure': np.mean(all_exposures) if all_exposures else 0,
            'max_exposure': np.max(all_exposures) if all_exposures else 0,
            'mean_rank': np.mean(all_ranks) if all_ranks else 0,
            'exposure_by_repetition': {
                rep: {
                    'mean': np.mean(exps),
                    'std': np.std(exps),
                    'count': len(exps)
                }
                for rep, exps in exposures_by_rep.items()
            },
            'individual_results': {
                cid: {
                    'rank': r.rank,
                    'exposure': r.exposure,
                    'success': r.success,
                    'repetitions': self.canary_manager.canaries[cid].repetitions
                }
                for cid, r in results.items()
            }
        }
        
        return summary
    
    def prefix_attack(
        self,
        canary_id: str,
        prefix_fraction: float = 0.5,
        beam_width: int = 10
    ) -> Dict[str, Any]:
        """
        Attack by giving a prefix and checking if model completes correctly.
        
        Args:
            canary_id: ID of canary to attack
            prefix_fraction: Fraction of canary to use as prefix
            beam_width: Beam width for generation
            
        Returns:
            Attack result dictionary
        """
        canary = self.canary_manager.canaries[canary_id]
        prefix_len = int(len(canary.sequence) * prefix_fraction)
        prefix = canary.sequence[:prefix_len]
        suffix = canary.sequence[prefix_len:]
        max_length = getattr(self.model, "max_length", 512)
        encoded_prefix = encode_sequence(
            self.tokenizer, prefix, max_length, return_tensors=True
        )
        prefix_ids = encoded_prefix["input_ids"].unsqueeze(0)
        # Number of tokens to generate (approximate for k-mer tokenizers)
        suffix_enc = encode_sequence(
            self.tokenizer, suffix, max_length, return_tensors=True
        )
        remaining_len = suffix_enc["attention_mask"].sum().item()
        if remaining_len <= 0:
            remaining_len = max(1, len(suffix) // 6)  # fallback for k-mer
        
        # Generate completions
        completions = self.beam_search_generate(
            prefix_ids, remaining_len, beam_width
        )
        
        # Decode and check
        generated_suffixes = []
        for seq_ids, log_prob in completions:
            decoded = self.tokenizer.decode(seq_ids[0].tolist())
            generated_suffix = decoded[len(prefix):]
            generated_suffixes.append((generated_suffix, log_prob))
        
        # Check if true suffix is in completions
        ranks_of_true = [
            i + 1 for i, (s, _) in enumerate(generated_suffixes) 
            if s == suffix
        ]
        
        return {
            'canary_id': canary_id,
            'prefix': prefix,
            'true_suffix': suffix,
            'top_completions': generated_suffixes[:5],
            'true_suffix_found': len(ranks_of_true) > 0,
            'true_suffix_rank': ranks_of_true[0] if ranks_of_true else -1
        }
