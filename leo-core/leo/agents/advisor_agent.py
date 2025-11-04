"""Advisor agent producing actionable suggestions."""
from __future__ import annotations

import os
from typing import List

try:  # pragma: no cover - optional dependency path
    from openai import OpenAI
    from openai import OpenAIError
except Exception:  # pragma: no cover - when openai isn't installed
    OpenAI = None  # type: ignore
    OpenAIError = Exception  # type: ignore

from ..state import LeoState

DEFAULT_SUGGESTIONS = [
    "Improve structured data coverage for richer search previews.",
    "Strengthen semantic consistency across key landing pages.",
    "Add internal links to highlight high-value content clusters.",
]

ADVISOR_MODEL = os.getenv("LEO_ADVISOR_MODEL", "gpt-4o-mini")


def _advisor_prompt(state: LeoState) -> str:
    metrics_summary = ", ".join(f"{key}: {value}" for key, value in state.metrics.items()) or "No metrics collected"
    return (
        "You are Leo, an AI visibility expert. Based on the following metrics and score, "
        "provide three concise recommendations to improve the site's search visibility."
        f"\nURL: {state.url}\nLeoRank: {state.leo_rank}\nMetrics: {metrics_summary}\n"
        "Respond with a numbered list."
    )


def _call_openai(state: LeoState) -> List[str] | None:
    if OpenAI is None:
        return None
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=ADVISOR_MODEL,
            messages=[
                {"role": "system", "content": "You are an SEO assistant."},
                {"role": "user", "content": _advisor_prompt(state)},
            ],
            max_tokens=300,
        )
        content = response.choices[0].message.content if response.choices else ""
        if not content:
            return None
        suggestions = []
        for line in content.splitlines():
            line = line.strip()
            if not line:
                continue
            if line[0].isdigit():
                line = line.split(".", 1)[-1].strip()
            suggestions.append(line)
        return suggestions[:3] if suggestions else None
    except OpenAIError:
        return None
    except Exception:
        return None


def run(state: LeoState) -> LeoState:
    """Attach AI-generated or static recommendations to the Leo state."""
    suggestions = _call_openai(state) or list(DEFAULT_SUGGESTIONS)
    return state.copy(update={"suggestions": suggestions})


__all__ = ["run", "DEFAULT_SUGGESTIONS"]
