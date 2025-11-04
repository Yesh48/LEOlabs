"""Scoring agent combining metrics into LeoRank."""
from __future__ import annotations

from ..state import LeoState


def run(state: LeoState) -> LeoState:
    """Calculate the LeoRank aggregate score."""
    metrics = dict(state.metrics)
    structure = metrics.get("structure", 0.0)
    semantic = metrics.get("semantic", 0.0)
    leo_rank = round(100 * (0.5 * structure + 0.5 * semantic), 2)

    return state.copy(update={"leo_rank": leo_rank, "metrics": metrics})


__all__ = ["run"]
