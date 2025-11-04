"""FastAPI server exposing Leo Core functionality."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query

from leo.db import get_database
from leo.graph import run_pipeline
from leo.utils.report_utils import state_to_report

app = FastAPI(title="Leo Core API", version="0.2.0")


@app.on_event("startup")
def _startup() -> None:
    get_database()


@app.get("/healthz", tags=["system"])
def healthcheck() -> dict[str, str]:
    """Basic health check endpoint."""
    summary = get_database().summary()
    return {"status": "ok", "db_engine": summary["engine"]}


@app.get("/audit", tags=["audit"])
def audit(url: str = Query(..., description="URL to audit"), persist: bool = Query(True)) -> dict:
    """Run the Leo pipeline on the provided URL and return the report."""
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    state = run_pipeline(url, persist=persist)
    return state_to_report(state)


@app.get("/metrics", tags=["metrics"])
def metrics(limit: int = Query(10, ge=1, le=100)) -> dict:
    """Return stored metrics and recent scores."""
    database = get_database()
    return {"summary": database.summary(), "recent": database.recent_scores(limit=limit)}
