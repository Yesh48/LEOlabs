"""State models for Leo Core."""
from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class LeoState(BaseModel):
    """Container for the Leo pipeline state."""

    url: str = Field(..., description="Target URL for the audit")
    html: Optional[str] = Field(default=None, description="Raw HTML fetched from the page")
    text: Optional[str] = Field(default=None, description="Visible text extracted from the HTML")
    metrics: Dict[str, float] = Field(default_factory=dict, description="Computed metric scores")
    leo_rank: Optional[float] = Field(default=None, description="Aggregate LeoRank score")
    suggestions: List[str] = Field(default_factory=list, description="List of advisor suggestions")


__all__ = ["LeoState"]
