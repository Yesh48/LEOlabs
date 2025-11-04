"""
cli.py
Command-line interface for LEO Core — powered by Typer.
Supports running audits, listing recent scores, and serving the FastAPI API or MCP server.
"""

import typer
import uvicorn
from leo.graph import run_pipeline
from leo.db import get_recent_scores
from leo.mcp.server import start_mcp_server

app = typer.Typer(help="LEO Core — AI Visibility Scoring CLI")


@app.command()
def audit(url: str):
    """Run full LEO audit pipeline for a given URL."""
    typer.echo(f"🔍 Auditing {url} ...")
    try:
        result = run_pipeline(url)
        typer.echo(f"✅ LEO Rank: {result.leo_rank}")
        typer.echo("�� Metrics:")
        for k, v in result.metrics.items():
            typer.echo(f"  {k}: {v}")
        typer.echo("\n💡 Suggestions:")
        for s in result.suggestions:
            typer.echo(f"  - {s}")
    except Exception as e:
        typer.echo(f"❌ Error: {e}")


@app.command()
def recent(limit: int = 10):
    """Display recent audit results from DB."""
    typer.echo(f"📈 Showing last {limit} results:")
    try:
        rows = get_recent_scores(limit)
        for r in rows:
            if isinstance(r, dict):
                typer.echo(f"{r['timestamp']} | {r['url']} | Rank: {r['rank']}")
            else:
                typer.echo(f"{r[2]} | {r[0]} | Rank: {r[1]}")
    except Exception as e:
        typer.echo(f"❌ Error: {e}")


@app.command()
def serve(host: str = "0.0.0.0", port: int = 8000):
    """Run the FastAPI server."""
    typer.echo(f"🚀 Starting API server at http://{host}:{port}")
    uvicorn.run("api.server:app", host=host, port=port)


@app.command()
def mcp(port: int = 8800):
    """Run the MCP server for GPT-native access."""
    typer.echo(f"🧩 Launching MCP server on port {port}")
    start_mcp_server(port=port)


if __name__ == "__main__":
    app()
