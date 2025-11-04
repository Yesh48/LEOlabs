"""Typer-based CLI entrypoint for Leo Core."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

import typer

from leo.db import get_database
from leo.graph import run_audit
from leo.utils.report_utils import save_report, state_to_report

app = typer.Typer(help="Leo Core command line interface")


def _slugify(url: str) -> str:
    cleaned = re.sub(r"^https?://", "", url).strip("/")
    slug = re.sub(r"[^A-Za-z0-9]+", "-", cleaned).strip("-")
    return slug or "report"


@app.command()
def audit(
    url: str,
    output: Optional[Path] = typer.Option(None, help="Optional path to store the report"),
    persist: bool = typer.Option(True, help="Persist results to the configured database"),
) -> None:
    """Audit a URL using the Leo pipeline."""
    typer.echo(f"Auditing {url}...")
    state = run_audit(url, persist=persist)
    report = state_to_report(state)
    typer.echo(json.dumps(report, indent=2))

    if output is None:
        output = Path("examples") / f"{_slugify(url)}.json"
    save_report(state, output)
    typer.echo(f"Report saved to {output.resolve()}")


@app.command()
def recent(limit: int = typer.Option(10, help="Number of recent scores to display")) -> None:
    """Display recent LeoRank scores."""
    database = get_database()
    for row in database.recent_scores(limit=limit):
        typer.echo(f"{row['timestamp']}: {row['url']} → {row['rank']}")


@app.command()
def serve(host: str = "0.0.0.0", port: int = 8000) -> None:
    """Launch the FastAPI service."""
    import uvicorn

    uvicorn.run("api.server:app", host=host, port=port, reload=False)


@app.command()
def mcp(host: str = "0.0.0.0", port: int = 8800) -> None:
    """Start the MCP server for GPT-native integrations."""
    from leo.mcp.server import serve as serve_mcp

    serve_mcp(host=host, port=port)


if __name__ == "__main__":
    app()
