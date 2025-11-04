from dataclasses import dataclass

import pytest

from leo import db as leo_db
from leo.graph import run_pipeline


SAMPLE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="description" content="Sample page for Leo tests">
  <meta name="keywords" content="ai, visibility, langgraph">
  <meta property="og:title" content="Sample">
  <meta property="og:description" content="Sample description">
  <script>console.log('ignore me');</script>
</head>
<body>
  <article itemtype="https://schema.org/Article">
    <h1>Visibility Matters</h1>
    <p>Leo ensures your most important content is readable by large language models.</p>
    <h2>Semantic Consistency</h2>
    <p>This paragraph reiterates key terms about semantic structure and discoverability.</p>
    <a href="/one">One</a>
    <a href="/two">Two</a>
  </article>
</body>
</html>
"""


@dataclass
class _FakeResponse:
    text: str


@pytest.fixture(autouse=True)
def reset_database(monkeypatch, tmp_path):
    db_path = tmp_path / "leo-test.db"
    monkeypatch.setenv("LEO_DB_PATH", str(db_path))
    monkeypatch.delenv("POSTGRES_ENABLED", raising=False)
    monkeypatch.setattr(leo_db, "_DB_INSTANCE", None, raising=False)
    yield
    monkeypatch.setattr(leo_db, "_DB_INSTANCE", None, raising=False)


def test_pipeline_runs_and_persists(monkeypatch):
    monkeypatch.setattr("leo.agents.crawler_agent._fetch", lambda url, timeout=10: _FakeResponse(SAMPLE_HTML))

    state = run_pipeline("https://example.com/visibility", persist=True)

    assert state.html is not None
    assert state.text is not None
    assert state.metrics["structure"] > 0
    assert state.metrics["semantic"] >= 0
    assert state.metrics["retrieval"] > 0

    expected_rank = round(
        100
        * (
            0.4 * state.metrics["structure"]
            + 0.4 * state.metrics["semantic"]
            + 0.2 * state.metrics["retrieval"]
        ),
        2,
    )
    assert state.leo_rank == expected_rank

    recent = leo_db.get_database().recent_scores(limit=1)
    assert recent, "Score was not persisted"
    assert recent[0]["url"] == "https://example.com/visibility"
    assert recent[0]["rank"] == pytest.approx(state.leo_rank)
