from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class LeoState(BaseModel):
    url: str
    html: Optional[str] = None
    metrics: Dict[str, float] = Field(default_factory=dict, description="Computed metrics for this audit")
    leo_rank: float = Field(default=0.0, description="Aggregated visibility score (0–100)")
    suggestions: List[str] = Field(default_factory=list, description="AI-generated improvement suggestions")
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="Audit timestamp in UTC."
    )
