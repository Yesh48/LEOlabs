# Leo Core

Leo Core is the foundational service for **LeoRank**, an AI-driven visibility scoring platform built on LangGraph agent pipelines. This repository ships version 0.1.0 of the core scoring engine, providing a unified CLI, REST API, Docker image, and Helm chart for Kubernetes deployments.

## Features
- 🕸️ Multi-agent pipeline that crawls, analyses structure, evaluates semantic coherence, scores pages, and produces advisor suggestions.
- 🛠️ Unified execution across CLI (`python cli.py audit <url>`), FastAPI (`uvicorn api.server:app`), Docker, and Helm deployments.
- 📊 Deterministic stub embeddings and scoring suitable for local development without external API dependencies.

## Architecture
The Leo pipeline is orchestrated by LangGraph and progresses through the following agents:
1. **Crawler Agent** – Fetches remote HTML and extracts visible text.
2. **Structure Agent** – Reviews markup quality (meta, OpenGraph, schema) and produces a normalized structure score.
3. **Semantic Agent** – Splits content into manageable chunks, computes stub embeddings, and measures semantic consistency.
4. **Scoring Agent** – Combines metrics into a 0-100 LeoRank value.
5. **Advisor Agent** – Emits actionable recommendations for improving visibility.

All state is tracked using the `LeoState` Pydantic model, enabling consistent serialization and validation across surfaces.

## Getting Started
Clone the repository and create a Python virtual environment, then install dependencies:

```bash
pip install -r requirements.txt
```

Run the CLI audit command:

```bash
python cli.py audit https://openai.com
```

### API Server
Start the FastAPI server with Uvicorn:

```bash
uvicorn api.server:app
```

Visit `http://localhost:8000/docs` for interactive documentation.

### Docker
Build a local Docker image:

```bash
docker build -t leo-core:0.1.0 .
```

Run the container (binding port 8000):

```bash
docker run --rm -p 8000:8000 leo-core:0.1.0
```

### Helm Deployment
Install the Helm chart into the `leo` namespace:

```bash
helm install leo-core charts/leo-core -n leo
```

Override configuration values as needed via `values.yaml` or `--set` flags.

## Example Output
Sample report (truncated) stored at `examples/sample_report.json` shows the JSON payload produced by the pipeline, including structure and semantic metrics plus the aggregated LeoRank score.

## Contributing
1. Fork the repository and create feature branches from `main`.
2. Follow existing coding conventions and ensure lint/test suites pass.
3. Submit a pull request describing your changes, test coverage, and deployment impact.

Issues and feature requests are welcome via GitHub.

## License
This project is released under the Apache 2.0 License. See `LICENSE` (to be added) for details.
