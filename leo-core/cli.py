"""Typer-based CLI entrypoint for Leo Core."""
from __future__ import annotations

import json
import re
from pathlib import Path

import typer

from leo.graph import run_graph
from leo.utils.report_utils import save_report, state_to_report

app = typer.Typer(help="Leo Core command line interface")


def _slugify(url: str) -> str:
    cleaned = re.sub(r"^https?://", "", url).strip("/")
    slug = re.sub(r"[^A-Za-z0-9]+", "-", cleaned).strip("-")
    return slug or "report"


@app.command()
def audit(url: str, output: Path = typer.Option(None, help="Optional path to store the report")) -> None:
    """Audit a URL using the Leo pipeline."""
    typer.echo(f"Auditing {url}...")
    state = run_graph(url)
    report = state_to_report(state)
    typer.echo(json.dumps(report, indent=2))

    if output is None:
        output = Path("examples") / f"{_slugify(url)}.json"
    save_report(state, output)
    typer.echo(f"Report saved to {output.resolve()}")


if __name__ == "__main__":
    app()
