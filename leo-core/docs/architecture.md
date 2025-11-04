# 🧱 LEO Core Architecture

LEO Core is a modular **AI Visibility Scoring Engine** built on a LangGraph-style agent pipeline.

---

## 🧩 Overview

Each website audit flows through 5 stages:

1. **CrawlerAgent** → Fetches and extracts raw HTML & text.
2. **StructureAgent** → Evaluates metadata, alt tags, and structural completeness.
3. **SemanticAgent** → Measures content clarity, keyword richness, and embedding similarity.
4. **ScoringAgent** → Aggregates results into a `LeoRank` (0–100).
5. **AdvisorAgent** → Suggests actionable improvements (GPT-powered or static fallback).

---

## ⚙️ System Components

| Component | Description |
|------------|-------------|
| `leo/state.py` | Shared pipeline state across all agents |
| `leo/graph.py` | Orchestration logic linking all agents |
| `leo/db.py` | SQLite or Postgres backend |
| `api/server.py` | FastAPI microservice exposing REST API |
| `cli.py` | Typer CLI for local audits or server runs |
| `leo/mcp/server.py` | MCP-compatible server for GPT-native integration |
| `charts/leo-core` | Helm chart for Kubernetes deployment |
| `brew/` | Homebrew formula for macOS users |

---

## 🧠 LangGraph Workflow
    A[CrawlerAgent] --> B[StructureAgent]
    B --> C[SemanticAgent]
    C --> D[ScoringAgent]
    D --> E[AdvisorAgent]
    E --> F[(Database)]
Each agent updates a shared LeoState object, passed sequentially through the pipeline.

☸️ Deployment Targets
Method	Description
Helm	Deploys to Kubernetes with optional CronJob & Postgres
Docker	Run locally or in CI pipelines
Brew	macOS installation for CLI tools
MCP Server	GPT-native access to scoring endpoints

🧪 Example Data Flow
leo audit https://openai.com
➡️ Runs all agents →
➡️ Stores url, rank, timestamp in DB →
➡️ Serves via FastAPI /metrics

🗃️ Data Schema
Table	Columns
scores	url TEXT, rank FLOAT, timestamp TEXT

🔐 Environment Variables
Variable	Description
OPENAI_API_KEY	Used by Semantic/Advisor agents
LEO_DB_ENGINE	sqlite or postgres
LEO_SQLITE_PATH	Path for SQLite DB
LEO_PG_HOST	Postgres hostname
LEO_PG_USER	Postgres username
LEO_PG_PASSWORD	Postgres password
LEO_PG_DATABASE	Postgres DB name

🧩 Scaling Roadmap
 Add async pipeline execution

 Introduce multi-agent concurrency via Celery/NATS

 Expand scoring features (accessibility, schema.org presence)

 Add GPT-eval dataset for benchmarked AI visibility

