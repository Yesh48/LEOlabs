"""Utilities for generating Leo Core reports."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from ..state import LeoState


def state_to_report(state: LeoState) -> Dict[str, Any]:
    """Convert a LeoState into a serializable report dictionary."""
    return {
        "url": state.url,
        "metrics": state.metrics,
        "leo_rank": state.leo_rank,
        "suggestions": state.suggestions,
        "html_present": bool(state.html),
        "text_length": len(state.text or ""),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def save_report(state: LeoState, output_path: Path) -> Path:
    """Persist a Leo report to disk as JSON."""
    report = state_to_report(state)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2))
    return output_path


__all__ = ["state_to_report", "save_report"]
