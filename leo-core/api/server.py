"""FastAPI server exposing Leo Core functionality."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query

from leo.graph import run_graph
from leo.utils.report_utils import state_to_report

app = FastAPI(title="Leo Core API", version="0.1.0")


@app.get("/health", tags=["system"])
def healthcheck() -> dict[str, str]:
    """Basic health check endpoint."""
    return {"status": "ok"}


@app.get("/audit", tags=["audit"])
def audit(url: str = Query(..., description="URL to audit")) -> dict:
    """Run the Leo pipeline on the provided URL and return the report."""
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    state = run_graph(url)
    return state_to_report(state)
