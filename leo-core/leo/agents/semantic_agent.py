"""Semantic agent for evaluating content coherence."""
from __future__ import annotations

from ..state import LeoState
from ..utils.metrics_utils import average_cosine_similarity, chunk_text, embed_texts


def run(state: LeoState) -> LeoState:
    """Compute semantic consistency metric."""
    chunks = chunk_text(state.text or "")
    embeddings = embed_texts(chunks)
    semantic_score = average_cosine_similarity(embeddings)

    metrics = dict(state.metrics)
    metrics["semantic"] = round(float(semantic_score), 4)

    return state.copy(update={"metrics": metrics})


__all__ = ["run"]
