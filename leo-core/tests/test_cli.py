"""CLI integration tests."""
from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from leo.state import LeoState

import cli


runner = CliRunner()


def test_audit_command_writes_report(tmp_path: Path, monkeypatch) -> None:
    """CLI audit command should save report output."""

    def fake_run_graph(url: str) -> LeoState:  # noqa: ARG001
        return LeoState(
            url="https://example.com",
            metrics={"structure": 0.5, "semantic": 0.5},
            leo_rank=50.0,
            suggestions=["Test suggestion"],
            html="<html></html>",
            text="Example text",
        )

    monkeypatch.setattr(cli, "run_graph", fake_run_graph)

    output_path = tmp_path / "report.json"
    result = runner.invoke(cli.app, ["audit", "https://example.com", "--output", str(output_path)])

    assert result.exit_code == 0
    assert output_path.exists()
    data = json.loads(output_path.read_text())
    assert data["leo_rank"] == 50.0
