# Leo Core

Leo Core powers **LeoRank v0.2.0** – the open-source AI visibility scoring engine. It ships a LangGraph-driven agent pipeline, FastAPI microservice, MCP server, and deployment tooling so teams can run web visibility audits anywhere from a developer laptop to Kubernetes clusters.

## Highlights
- 🕸️ **LangGraph agent pipeline**: crawler → structure → semantic → scoring → advisor, sharing a typed `LeoState`.
- 🤖 **Hybrid AI execution**: automatic OpenAI embeddings & chat when `OPENAI_API_KEY` is set, with deterministic offline fallbacks when it is not.
- 🗃️ **Pluggable storage**: SQLite by default (`/tmp/leo.db`) with optional Postgres when environment variables/Helm values enable it.
- 🔌 **Multiple entry points**: Typer CLI (`leo audit`, `leo recent`, `leo serve`, `leo mcp`), FastAPI endpoints, and a TCP MCP server with tools (`leo_audit`, `leo_recent`).
- ☸️ **Production ready**: Dockerfile, Helm chart (with CronJob + MCP deployment + optional Postgres dependency), and Homebrew tap for macOS.

Metric weights, formulas, and sample outputs are documented in [`specs/leo-specs.yml`](specs/leo-specs.yml) for transparency.

## Installation
Create a Python 3.11+ environment and install dependencies:

```bash
pip install -r requirements.txt
```

### CLI Usage
```
leo audit https://openai.com
leo audit https://openai.com --no-persist  # skip DB write
leo recent --limit 5
leo serve --host 0.0.0.0 --port 8000
leo mcp --port 8800
```
Reports are written to `examples/<slug>.json` by default. Set `OPENAI_API_KEY` to enable real embeddings and advisor recommendations.

### API Server
Run the FastAPI service directly:

```bash
uvicorn api.server:app --reload
```

Endpoints:
- `GET /healthz` – liveness + DB engine info
- `GET /audit?url=https://openai.com` – execute an audit (persists by default)
- `GET /metrics?limit=10` – return summary statistics and recent scores

### Database Configuration
| Variable | Description | Default |
| --- | --- | --- |
| `LEO_DB_ENGINE` | `sqlite` or `postgres` | `sqlite` |
| `LEO_DB_PATH` | SQLite file path | `/tmp/leo.db` |
| `LEO_DB_DSN` | Postgres DSN (optional) | – |
| `LEO_DB_HOST`/`LEO_DB_PORT` | Postgres host/port | `leo-postgres` / `5432` |
| `LEO_DB_USER`/`LEO_DB_PASSWORD`/`LEO_DB_NAME` | Postgres credentials | `leo` / `leo123` / `leodb` |

### MCP Server
The lightweight TCP MCP server listens on port `8800` by default and supports newline-delimited JSON requests:

```bash
leo mcp --port 9900
# client request example
printf '{"id":1,"method":"leo_recent"}\n' | nc localhost 9900
```

Refer to `leo/mcp/config/manifest.json` when integrating with GPT-native runtimes.

### Docker
Build and run the container:

```bash
docker build -t leo-core:0.2.0 .
docker run --rm -p 8000:8000 -e OPENAI_API_KEY=$OPENAI_API_KEY leo-core:0.2.0
```

### Helm Deployment
Update chart dependencies and install:

```bash
helm dependency update charts/leo-core
helm install leo-core charts/leo-core \
  -n leo --create-namespace \
  --set env.OPENAI_API_KEY="sk-..." \
  --set db.postgres.enabled=true \
  --set mcp.enabled=true
```

The chart provisions:
- API `Deployment` + `Service`
- Optional MCP deployment (controlled by `mcp.enabled`)
- Optional Bitnami Postgres subchart + PVC when `db.postgres.enabled=true`
- `CronJob` for scheduled re-audits (`cronjob.schedule` & `cronjob.urls`)

### Homebrew (macOS)
Tap and install the CLI:

```bash
brew tap yesh48/leo
brew install leo-core
```

The formula installs the Python package and post-install script (`brew/postinstall.sh`) prompts for an `OPENAI_API_KEY`, storing it at `~/.leo/config`.

### Tests
Install extras and run the suite:

```bash
pip install .[test]
pytest
```

## Example Output
`examples/sample_report.json` contains a sample report emitted by the pipeline, including computed metrics, LeoRank, timestamp, and recommendations.

## Changelog
See [CHANGELOG.md](CHANGELOG.md) for version history (v0.2.0 highlights: MCP server, CronJob support, Postgres integration, Helm/Homebrew updates).

## Contributing & License
Community contributions are welcome—review [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines. Leo Core is released under the [Apache 2.0 License](LICENSE).
