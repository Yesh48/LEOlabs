"""Unit tests for individual Leo agents."""
from dataclasses import dataclass

import pytest

from leo import db as leo_db
from leo.agents import advisor_agent, crawler_agent, scoring_agent, semantic_agent, structure_agent
from leo.state import LeoState
from leo.utils.html_utils import extract_visible_text


SAMPLE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"description\" content=\"Agent test\">
  <meta property=\"og:title\" content=\"Agent Sample\">
  <script>console.log('ignore');</script>
</head>
<body>
  <main itemtype=\"https://schema.org/Article\">
    <h1>Agent Coverage</h1>
    <h2>Structure Metrics</h2>
    <p>This sample ensures every agent can process the shared state.</p>
    <a href=\"/alpha\">Alpha</a>
    <a href=\"/beta\">Beta</a>
  </main>
</body>
</html>
"""


@dataclass
class _FakeResponse:
    text: str


@pytest.fixture(autouse=True)
def reset_database(monkeypatch, tmp_path):
    db_path = tmp_path / "leo-agent-tests.db"
    monkeypatch.setenv("LEO_DB_PATH", str(db_path))
    monkeypatch.delenv("POSTGRES_ENABLED", raising=False)
    monkeypatch.setattr(leo_db, "_DB_INSTANCE", None, raising=False)
    yield
    monkeypatch.setattr(leo_db, "_DB_INSTANCE", None, raising=False)


def test_crawler_populates_html_and_text(monkeypatch):
    monkeypatch.setattr("leo.agents.crawler_agent._fetch", lambda url, timeout=10: _FakeResponse(SAMPLE_HTML))
    state = LeoState(url="https://example.com")

    result = crawler_agent.run(state)

    assert result.html and "Agent Coverage" in result.html
    assert result.text and "Structure Metrics" in result.text


def test_structure_agent_scores_markup():
    state = LeoState(url="https://example.com", html=SAMPLE_HTML, text=extract_visible_text(SAMPLE_HTML))

    result = structure_agent.run(state)

    assert "structure" in result.metrics
    assert 0.0 <= result.metrics["structure"] <= 1.0


def test_semantic_agent_generates_similarity(monkeypatch):
    # Force deterministic fallback embeddings.
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    text = extract_visible_text(SAMPLE_HTML)
    state = LeoState(url="https://example.com", html=SAMPLE_HTML, text=text)

    result = semantic_agent.run(state)

    assert "semantic" in result.metrics
    assert 0.0 <= result.metrics["semantic"] <= 1.0


def test_scoring_agent_combines_metrics_and_persists():
    text = extract_visible_text(SAMPLE_HTML)
    base_state = LeoState(
        url="https://example.com",
        html=SAMPLE_HTML,
        text=text,
        metrics={"structure": 0.8, "semantic": 0.75},
    )

    result = scoring_agent.run(base_state, persist=True)

    assert result.leo_rank is not None
    assert result.metrics["retrieval"] > 0

    recent = leo_db.get_database().recent_scores(limit=1)
    assert recent
    assert recent[0]["url"] == "https://example.com"


def test_advisor_agent_uses_fallback(monkeypatch):
    monkeypatch.setattr("leo.agents.advisor_agent._call_openai", lambda state: None)
    state = LeoState(
        url="https://example.com",
        metrics={"structure": 0.8, "semantic": 0.75, "retrieval": 0.6},
        leo_rank=82.0,
    )

    result = advisor_agent.run(state)

    assert result.suggestions
    assert result.suggestions == advisor_agent.DEFAULT_SUGGESTIONS

