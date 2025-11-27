import time
import difflib
from typing import Tuple
from transformers import PreTrainedTokenizerBase


def measure_latency(func):
    """
    Decorator to measure latency in ms of a function call.
    Returns (result, latency_ms).
    """
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        latency_ms = (end - start) * 1000.0
        return result, latency_ms
    return wrapper


def compute_diff(original: str, fixed: str, from_name="vulnerable", to_name="fixed") -> str:
    original_lines = original.splitlines(keepends=True)
    fixed_lines = fixed.splitlines(keepends=True)
    diff_lines = difflib.unified_diff(
        original_lines,
        fixed_lines,
        fromfile=from_name,
        tofile=to_name,
        lineterm=""
    )
    return "".join(diff_lines)


def count_tokens(tokenizer: PreTrainedTokenizerBase, text: str) -> int:
    if tokenizer is None:
        # Fallback approximate count if tokenizer is unavailable
        return len(text.split())
    encoded = tokenizer(text, return_tensors=None)
    return len(encoded["input_ids"])
