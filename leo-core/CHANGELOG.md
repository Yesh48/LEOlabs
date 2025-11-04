# Changelog

## v0.2.0
- Added MCP TCP server exposing `leo_audit` and `leo_recent` tools with manifest metadata.
- Introduced SQLite/Postgres persistence layer with CLI/API helpers for recent metrics.
- Expanded Helm chart: optional Postgres dependency, MCP deployment, CronJob, PVC, and configurable environment values.
- Added Homebrew tap assets for macOS installation (`brew/leo-core.rb`, `brew/postinstall.sh`).
- Updated CLI with `recent`, `serve`, and `mcp` commands alongside improved Typer UX.
- Enriched FastAPI service with `/healthz` and `/metrics` endpoints plus DB auto-initialisation.
- Refreshed documentation, sample outputs, and tests for the 0.2.0 release.
