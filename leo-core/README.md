# Leo Core v0.2 – AI Visibility Scoring Engine

![Build status](https://github.com/Yesh48/LEOlabs/actions/workflows/ci.yml/badge.svg)
![Version](https://img.shields.io/badge/version-0.2.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Leo Core is the reference implementation of the **LeoRank** visibility model. It orchestrates a LangGraph pipeline of specialist agents that crawl a website, measure structural readiness, evaluate semantic coherence, and surface GPT-powered guidance for improving Large Language Model visibility.

Version **0.2.0** introduces production-grade persistence, Helm + Homebrew distribution, an MCP server for GPT integrations, and the fully weighted LeoRank formula.

## Feature Highlights

- 🧠 **LangGraph pipeline** – Crawler → Structure → Semantic → Scoring → Advisor, all sharing a single `LeoState` snapshot.
- 🧮 **Weighted scoring** – Configurable weights (`leo/config/weights.yml`) and retrieval heuristics combine into the official LeoRank computation.
- 💾 **Database ready** – SQLite by default (`/tmp/leo.db`) with optional Postgres (`POSTGRES_ENABLED=true`), surfaced through the CLI, API, and MCP tools.
- 🌐 **Multi-surface access** – Typer CLI, FastAPI service, Docker image, LangGraph runner, and MCP transport for GPT-native workflows.
- ☸️ **Kubernetes friendly** – Helm chart with CronJob scheduling, optional Bitnami Postgres dependency, MCP sidecar, and OpenAI secret management.
- 🍺 **Homebrew tap** – Installable via `brew install leo-core`, including a guided post-install script for storing API keys.

## Pipeline Overview

```text
Crawler → Structure → Semantic → Scoring → Advisor
```

Each agent reads and writes a `LeoState` object so downstream logic has access to HTML, extracted text, computed metrics, and generated suggestions. The architecture diagram in [`docs/architecture.md`](docs/architecture.md) illustrates how data flows between agents, storage, and surfaces.

## Quick Start

Install Python requirements and run an audit locally:

```bash
pip install -r requirements.txt
python cli.py audit https://openai.com
```

### CLI Commands

```bash
leo audit <url>         # run the full pipeline and print/save a report
leo recent              # show the latest stored LeoRank entries
leo serve               # launch the FastAPI server
leo mcp                 # start the MCP server for GPT integrations
```

Reports are saved to `examples/<slug>.json` by default; pass `--output` to override and `--no-persist` to skip database writes.

### FastAPI Service

```bash
python cli.py serve
# or
uvicorn api.server:app --host 0.0.0.0 --port 8000
```

Available endpoints:

- `GET /audit?url=https://example.com` – run an on-demand audit (optional `persist=false`).
- `GET /metrics` – summary statistics plus recent scores.
- `GET /healthz` – readiness and DB engine information.

### Database Configuration

Environment variables control persistence:

- `LEO_DB_ENGINE=sqlite|postgres`
- `LEO_DB_PATH=/tmp/leo.db` (for SQLite)
- `POSTGRES_ENABLED=true` to force Postgres mode
- `LEO_DB_HOST`, `LEO_DB_PORT`, `LEO_DB_USER`, `LEO_DB_PASSWORD`, `LEO_DB_NAME`

SQLite is stored on disk, while Postgres requires `psycopg2-binary` and the above credentials.

### Docker Image

```bash
docker build -t leo-core:0.2.0 .
docker run --rm -p 8000:8000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e LEO_DB_ENGINE=sqlite leo-core:0.2.0
```

### Helm Deployment

```bash
helm install leo-core charts/leo-core -n leo --create-namespace \
  --set env.OPENAI_API_KEY="sk-..." \
  --set db.postgres.enabled=true \
  --set mcp.enabled=true
```

Key `values.yaml` sections:

- `image.*` – container registry coordinates.
- `env.OPENAI_API_KEY` – optional pre-populated secret value.
- `db.*` – switch between SQLite and Postgres (with optional PVCs).
- `cronjob.*` – schedule daily audits across a list of URLs.
- `mcp.*` – enable/disable the MCP deployment and port.

`charts/leo-core/templates/cronjob.yaml` runs the CLI nightly to keep metrics fresh, while `postgres-dependency.yaml` wires the Bitnami Postgres subchart when enabled.

### Homebrew Installation

```bash
brew tap yesh48/leo
brew install leo-core
export OPENAI_API_KEY="sk-..."
leo audit https://openai.com
```

The post-install hook stores your API key at `~/.leo/config` for convenient reuse.

### MCP Transport

`leo.mcp.server` hosts a TCP MCP endpoint with two tools:

- `leo_audit` – trigger a LangGraph audit and return the report JSON.
- `leo_recent` – fetch persisted scores.

Run via `leo mcp --host 0.0.0.0 --port 8800` or deploy the Helm subchart.

### Testing

```bash
pip install .[test]
pytest -v
```

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for coding standards, development workflow, and release guidelines. Issue and pull request templates live under [`.github/`](.github/) to help new contributors share context quickly.

### License

Leo Core is released under the [MIT License](LICENSE).
