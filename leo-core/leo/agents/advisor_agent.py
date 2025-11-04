"""Advisor agent producing actionable suggestions."""
from __future__ import annotations

from ..state import LeoState

DEFAULT_SUGGESTIONS = [
    "Improve structured data coverage for richer search previews.",
    "Strengthen semantic consistency across key landing pages.",
    "Add internal links to highlight high-value content clusters.",
]


def run(state: LeoState) -> LeoState:
    """Attach static recommendations to the Leo state."""
    return state.copy(update={"suggestions": list(DEFAULT_SUGGESTIONS)})


__all__ = ["run", "DEFAULT_SUGGESTIONS"]
