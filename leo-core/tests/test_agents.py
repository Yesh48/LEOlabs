"""Unit tests for Leo Core agents."""
from __future__ import annotations

from typing import Any

import pytest

from leo.agents import advisor_agent, crawler_agent, scoring_agent, semantic_agent, structure_agent
from leo.state import LeoState


class DummyResponse:
    """Simple response stub for crawler tests."""

    def __init__(self, text: str):
        self.text = text


def test_crawler_agent_populates_html_and_text(monkeypatch: pytest.MonkeyPatch) -> None:
    """Crawler agent should set html and text when fetch succeeds."""

    def fake_fetch(url: str, timeout: int = 10) -> Any:  # noqa: ARG001
        return DummyResponse("""<html><body><p>Hello world</p></body></html>""")

    monkeypatch.setattr(crawler_agent, "_fetch", fake_fetch)

    state = LeoState(url="https://example.com")
    result = crawler_agent.run(state)

    assert result.html is not None
    assert "Hello world" in (result.text or "")


def test_structure_agent_generates_normalized_score() -> None:
    """Structure agent should produce a structure metric between 0 and 1."""
    html = """
    <html>
      <head>
        <meta name=\"description\" content=\"Example\" />
        <meta property=\"og:title\" content=\"Example\" />
        <script type=\"application/ld+json\" itemtype=\"http://schema.org/Article\"></script>
      </head>
    </html>
    """
    state = LeoState(url="https://example.com", html=html)
    result = structure_agent.run(state)

    assert "structure" in result.metrics
    assert 0.0 <= result.metrics["structure"] <= 1.0


def test_semantic_agent_updates_metrics() -> None:
    """Semantic agent should add a semantic metric for non-empty text."""
    text = "This is a test. " * 40
    state = LeoState(url="https://example.com", text=text)
    result = semantic_agent.run(state)

    assert "semantic" in result.metrics
    assert 0.0 <= result.metrics["semantic"] <= 1.0


def test_scoring_agent_combines_metrics() -> None:
    """Scoring agent should compute leo_rank from metrics."""
    state = LeoState(url="https://example.com", metrics={"structure": 0.4, "semantic": 0.8})
    result = scoring_agent.run(state)

    assert result.leo_rank == pytest.approx(60.0)


def test_advisor_agent_returns_suggestions() -> None:
    """Advisor agent should attach default suggestions."""
    state = LeoState(url="https://example.com")
    result = advisor_agent.run(state)

    assert len(result.suggestions) == 3
