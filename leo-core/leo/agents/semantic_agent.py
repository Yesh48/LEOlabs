"""Semantic agent for evaluating content coherence."""
from __future__ import annotations

import os
from typing import Iterable, Optional

import numpy as np

try:  # pragma: no cover - optional dependency path
    from openai import OpenAI
    from openai import OpenAIError
except Exception:  # pragma: no cover - when openai isn't available at runtime
    OpenAI = None  # type: ignore
    OpenAIError = Exception  # type: ignore

from ..state import LeoState
from ..utils.metrics_utils import average_cosine_similarity, chunk_text, embed_texts

EMBEDDING_MODEL = os.getenv("LEO_EMBEDDING_MODEL", "text-embedding-3-small")


def _maybe_remote_embeddings(chunks: Iterable[str]) -> Optional[np.ndarray]:
    if OpenAI is None:
        return None
    chunk_list = list(chunks)
    if not chunk_list:
        return np.zeros((0, 0), dtype=float)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        client = OpenAI(api_key=api_key)
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=chunk_list)
        vectors = np.array([item.embedding for item in response.data], dtype=float)
        return vectors
    except OpenAIError:
        return None
    except Exception:
        return None


def run(state: LeoState) -> LeoState:
    """Compute semantic consistency metric."""
    chunks = chunk_text(state.text or "")
    remote_embeddings = _maybe_remote_embeddings(chunks)
    if remote_embeddings is not None and remote_embeddings.size > 0:
        embeddings = remote_embeddings
    else:
        embeddings = embed_texts(chunks)
    semantic_score = average_cosine_similarity(embeddings)

    metrics = dict(state.metrics)
    metrics["semantic"] = round(float(semantic_score), 4)

    return state.copy(update={"metrics": metrics})


__all__ = ["run"]
