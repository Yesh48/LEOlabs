from dataclasses import dataclass

import pytest
from fastapi.testclient import TestClient

from api.server import app
from leo import db as leo_db

SAMPLE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="description" content="API sample for Leo tests">
  <meta property="og:title" content="API Sample">
</head>
<body>
  <article itemtype="https://schema.org/Article">
    <h1>API Audit Fixture</h1>
    <p>This content feeds the FastAPI integration test so that structure and semantic metrics are populated.</p>
    <a href="/alpha">Alpha</a>
  </article>
</body>
</html>
"""


@dataclass
class _FakeResponse:
    text: str


@pytest.fixture(autouse=True)
def reset_database(monkeypatch, tmp_path):
    db_path = tmp_path / "leo-api-test.db"
    monkeypatch.setenv("LEO_DB_PATH", str(db_path))
    monkeypatch.delenv("POSTGRES_ENABLED", raising=False)
    monkeypatch.setattr(leo_db, "_DB_INSTANCE", None, raising=False)
    yield
    monkeypatch.setattr(leo_db, "_DB_INSTANCE", None, raising=False)


def test_audit_endpoint_and_metrics(monkeypatch):
    monkeypatch.setattr("leo.agents.crawler_agent._fetch", lambda url, timeout=10: _FakeResponse(SAMPLE_HTML))

    with TestClient(app) as client:
        response = client.get("/audit", params={"url": "https://example.com"})
        assert response.status_code == 200
        payload = response.json()
        assert payload["leo_rank"] >= 0
        assert payload["metrics"]["structure"] > 0

        metrics_response = client.get("/metrics")
        assert metrics_response.status_code == 200
        metrics_payload = metrics_response.json()
        assert metrics_payload["summary"]["count"] >= 1

        health_response = client.get("/healthz")
        assert health_response.status_code == 200
        assert health_response.json()["status"] == "ok"
