"""Answer extraction and scoring helpers for geometry-style outputs."""
from __future__ import annotations

import re


_BOX_RE = re.compile(r"\\boxed\{([^{}]+)\}|boxed\{([^{}]+)\}", re.IGNORECASE)
_ANSWER_RE = re.compile(r"(?:answer|final answer|答案)\s*(?:is|:|=)?\s*([A-Za-z]|\-?\d+(?:\.\d+)?)", re.IGNORECASE)
_NUMBER_RE = re.compile(r"-?\d+(?:\.\d+)?")


def normalize_answer(text: str) -> str:
    """Normalize final answers for exact, deterministic comparison."""
    value = str(text).strip().lower()
    value = value.replace("\\", "")
    value = re.sub(r"\s+", " ", value)
    value = value.strip(" .。,:;，；")
    if len(value) >= 2 and value[0] in "([{" and value[-1] in ")]}":
        value = value[1:-1].strip()
    return value


def extract_final_answer(text: str) -> str:
    """Extract the most likely final answer from a model response."""
    raw = str(text)
    boxed = _BOX_RE.findall(raw)
    if boxed:
        left, right = boxed[-1]
        return normalize_answer(left or right)

    answer = _ANSWER_RE.findall(raw)
    if answer:
        return normalize_answer(answer[-1])

    numbers = _NUMBER_RE.findall(raw)
    if numbers:
        return normalize_answer(numbers[-1])

    stripped = normalize_answer(raw)
    if len(stripped) == 1 and stripped.isalpha():
        return stripped
    return stripped


def score_ground_truth(prediction: str, answer: str) -> bool:
    """Compare model prediction against geometry3k ground truth."""
    return extract_final_answer(prediction) == extract_final_answer(answer)


def score_sync_async_consistency(sync_answer: str, async_answer: str) -> bool:
    """Compare paired sync/async answers after the same normalization."""
    return extract_final_answer(sync_answer) == extract_final_answer(async_answer)
