"""
api/server.py
FastAPI service for LEO Core — exposes endpoints to run audits and retrieve results.
"""

from fastapi import FastAPI, Query
from leo.graph import run_pipeline
from leo.db import get_recent_scores
from leo.state import LeoState

app = FastAPI(
    title="LEO Core API",
    description="AI Visibility Scoring Engine (LangGraph + FastAPI)",
    version="0.2.0",
)


@app.get("/healthz")
def health_check():
    """Simple liveness check."""
    return {"status": "ok", "version": "0.2.0"}


@app.get("/audit")
def audit_url(url: str = Query(..., description="Target website URL to audit")):
    """Run full LEO audit pipeline for a given URL."""
    try:
        result: LeoState = run_pipeline(url)
        return {
            "url": result.url,
            "metrics": result.metrics,
            "leo_rank": result.leo_rank,
            "suggestions": result.suggestions,
            "timestamp": result.timestamp,
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/metrics")
def get_metrics(limit: int = 10):
    """Return recent audit scores."""
    try:
        rows = get_recent_scores(limit)
        return {"results": [dict(row) for row in rows]}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.server:app", host="0.0.0.0", port=8000)
