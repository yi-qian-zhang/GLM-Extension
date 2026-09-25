"""Pilot harness for the tokenizer x objective memorization study.

Standalone: pure PyTorch, no dependency on src/. Everything is per-nucleotide
and the uniform-DNA entropy floor (4.0 perplexity / 2.000 bits per nt) is a
standing correctness check on every scorer.
"""
