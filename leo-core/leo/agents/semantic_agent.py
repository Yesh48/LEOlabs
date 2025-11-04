"""Semantic agent for evaluating content coherence."""
from __future__ import annotations

import os
from typing import Iterable, Optional

import numpy as np

try:  # pragma: no cover - optional dependency path
    import openai
    from openai import OpenAIError
except Exception:  # pragma: no cover - when openai isn't available at runtime
    openai = None  # type: ignore
    OpenAIError = Exception  # type: ignore

from ..state import LeoState
from ..utils.metrics_utils import average_cosine_similarity, chunk_text, embed_texts

EMBEDDING_MODEL = os.getenv("LEO_EMBEDDING_MODEL", "text-embedding-3-small")


def _maybe_remote_embeddings(chunks: Iterable[str]) -> Optional[np.ndarray]:
    if openai is None:
        return None
    chunk_list = list(chunks)
    if not chunk_list:
        return None
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        openai.api_key = api_key
        response = openai.embeddings.create(model=EMBEDDING_MODEL, input=chunk_list)
        data = getattr(response, "data", None) or []
        vector_list = []
        for item in data:
            embedding = getattr(item, "embedding", None)
            if embedding is None and isinstance(item, dict):
                embedding = item.get("embedding")
            if embedding is None:
                continue
            vector_list.append(embedding)
        if not vector_list:
            return None
        return np.array(vector_list, dtype=float)
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

    return state.model_copy(update={"metrics": metrics})


__all__ = ["run"]
