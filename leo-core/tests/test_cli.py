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

    def fake_run_audit(url: str, persist: bool = True) -> LeoState:  # noqa: ARG001
        assert persist is False
        return LeoState(
            url="https://example.com",
            metrics={"structure": 0.5, "semantic": 0.5},
            leo_rank=50.0,
            suggestions=["Test suggestion"],
            html="<html></html>",
            text="Example text",
        )

    monkeypatch.setattr(cli, "run_audit", fake_run_audit)

    output_path = tmp_path / "report.json"
    result = runner.invoke(
        cli.app,
        ["audit", "https://example.com", "--output", str(output_path), "--no-persist"],
    )

    assert result.exit_code == 0
    assert output_path.exists()
    data = json.loads(output_path.read_text())
    assert data["leo_rank"] == 50.0
    assert "generated_at" in data


def test_recent_command_lists_scores(monkeypatch) -> None:
    """Recent command should display stored scores."""

    class DummyDB:
        def recent_scores(self, limit: int = 10):  # noqa: ARG002
            return [
                {"timestamp": "2024-01-01T00:00:00", "url": "https://example.com", "rank": 88.0}
            ]

    monkeypatch.setattr(cli, "get_database", lambda: DummyDB())

    result = runner.invoke(cli.app, ["recent"])

    assert result.exit_code == 0
    assert "example.com" in result.stdout
