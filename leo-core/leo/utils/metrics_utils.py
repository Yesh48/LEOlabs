"""Metric utilities for Leo Core."""
from __future__ import annotations

from typing import Iterable, List

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def normalize_count(count: int, max_expected: int = 10) -> float:
    """Normalize a count to the 0-1 range using a soft upper bound."""
    if max_expected <= 0:
        return 0.0
    return max(0.0, min(count / float(max_expected), 1.0))


def text_richness(text: str, baseline: int = 2000) -> float:
    """Estimate textual richness as a function of length."""
    if baseline <= 0:
        return 0.0
    length = len(text.strip())
    if length <= 0:
        return 0.0
    return max(0.0, min(length / float(baseline), 1.0))


def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    """Split text into roughly equal sized chunks."""
    if not text:
        return []
    text = " ".join(text.split())
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


def embed_texts(chunks: Iterable[str], dimensions: int = 64) -> np.ndarray:
    """Generate deterministic stub embeddings for text chunks."""
    vectors = []
    for chunk in chunks:
        vector = np.zeros(dimensions, dtype=float)
        for index, char in enumerate(chunk.encode("utf-8")):
            vector[index % dimensions] += (char % 32) / 31.0
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector /= norm
        vectors.append(vector)
    if not vectors:
        return np.zeros((0, dimensions), dtype=float)
    return np.vstack(vectors)


def average_cosine_similarity(embeddings: np.ndarray) -> float:
    """Compute the average pairwise cosine similarity for embeddings."""
    if embeddings.size == 0:
        return 0.0
    if embeddings.shape[0] == 1:
        return 1.0
    similarity_matrix = cosine_similarity(embeddings)
    # Exclude self similarities by masking the diagonal
    n = embeddings.shape[0]
    mask = ~np.eye(n, dtype=bool)
    if mask.sum() == 0:
        return 0.0
    values = similarity_matrix[mask]
    return float(np.clip(values.mean(), 0.0, 1.0))


def compute_retrieval_score(
    text: str,
    heading_count: int,
    anchor_count: int,
) -> float:
    """Combine retrieval-oriented heuristics into a 0-1 score."""

    richness = text_richness(text, baseline=3000)
    heading_signal = normalize_count(heading_count, max_expected=12)
    anchor_signal = normalize_count(anchor_count, max_expected=60)

    score = (0.5 * richness) + (0.3 * heading_signal) + (0.2 * anchor_signal)
    return float(np.clip(score, 0.0, 1.0))


__all__ = [
    "normalize_count",
    "chunk_text",
    "embed_texts",
    "average_cosine_similarity",
    "text_richness",
    "compute_retrieval_score",
]
