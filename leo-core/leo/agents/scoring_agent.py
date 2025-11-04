"""Scoring agent combining metrics into LeoRank."""
from __future__ import annotations

import functools
from pathlib import Path
from typing import Dict

import yaml

from ..db import get_database
from ..state import LeoState
from ..utils.html_utils import parse_html
from ..utils.metrics_utils import compute_retrieval_score

_WEIGHTS_PATH = Path(__file__).resolve().parents[1] / "config" / "weights.yml"


@functools.lru_cache(maxsize=1)
def _load_weights() -> Dict[str, float]:
    default_weights = {"structure": 0.4, "semantic": 0.4, "retrieval": 0.2}
    try:
        data = yaml.safe_load(_WEIGHTS_PATH.read_text())
    except FileNotFoundError:
        return default_weights
    except Exception:
        return default_weights
    if not isinstance(data, dict):
        return default_weights
    weights: Dict[str, float] = {}
    for key, value in data.items():
        try:
            weights[key] = float(value)
        except (TypeError, ValueError):
            continue
    return {**default_weights, **weights}


def run(state: LeoState, persist: bool = True) -> LeoState:
    """Calculate the LeoRank aggregate score and persist it."""

    metrics = dict(state.metrics)
    soup = parse_html(state.html or "")
    heading_count = len(soup.find_all(["h1", "h2", "h3", "h4"]))
    anchor_count = len(soup.find_all("a"))
    retrieval_score = compute_retrieval_score(state.text or "", heading_count, anchor_count)
    metrics.setdefault("structure", 0.0)
    metrics.setdefault("semantic", 0.0)
    metrics["retrieval"] = round(retrieval_score, 4)

    weights = _load_weights()
    leo_rank = 100 * (
        weights.get("structure", 0.0) * metrics.get("structure", 0.0)
        + weights.get("semantic", 0.0) * metrics.get("semantic", 0.0)
        + weights.get("retrieval", 0.0) * metrics.get("retrieval", 0.0)
    )
    leo_rank = round(float(leo_rank), 2)

    updated_state = state.model_copy(update={"leo_rank": leo_rank, "metrics": metrics})
    if persist:
        try:
            get_database().record_score(url=state.url, rank=float(leo_rank))
        except Exception:
            # Persistence errors should not interrupt scoring flow.
            pass
    return updated_state


__all__ = ["run"]
