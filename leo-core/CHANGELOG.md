# Changelog

## v0.2.0
- Delivered full LangGraph production pipeline with crawler, structure, semantic, scoring, and advisor agents plus retrieval-aware LeoRank weights.
- Persist scores automatically from the ScoringAgent with SQLite default storage and optional Postgres via `POSTGRES_ENABLED`.
- Expanded FastAPI service, Typer CLI, and LangGraph helpers to expose `run_pipeline`, `/metrics`, `/healthz`, and MCP transport endpoints.
- Added MCP TCP server manifest, Helm chart enhancements (CronJob, MCP deployment, optional Bitnami Postgres dependency, PVCs, OpenAI secrets), and Homebrew installer assets.
- Regenerated documentation (`README.md`, `Agents.md`) and sample reports to reflect the 0.2 visibility scoring engine.
