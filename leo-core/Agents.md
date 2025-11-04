# 🧠 Overview
Leo Core quantifies a website's **AI visibility** — how easily Large Language Models can discover, retrieve, and reason over its content. Version 0.2 ships a five-agent LangGraph that audits markup quality, semantic coherence, and retrieval readiness before surfacing optimization guidance and persisting LeoRank scores.

# ⚙️ Pipeline
```
Crawler → Structure → Semantic → Scoring → Advisor
```
Each node receives and updates a shared `LeoState` instance so downstream agents see the latest HTML, extracted text, metrics, and suggestions.

# 🧩 Agent Descriptions

## CrawlerAgent (`leo/agents/crawler_agent.py`)
- **Purpose:** Fetch the target URL and extract readable text.
- **Inputs:** `state.url`
- **Outputs:** `state.html`, `state.text`
- **Logic:** Issues an HTTP GET with a Leo-specific user agent, then strips non-visible elements via BeautifulSoup utilities.
- **Example Metrics/Artifacts:** Raw HTML string, whitespace-normalized body text ready for analysis.

## StructureAgent (`leo/agents/structure_agent.py`)
- **Purpose:** Score the richness of discoverability markup.
- **Inputs:** `state.html`
- **Outputs:** `state.metrics["structure"]`
- **Logic:** Parses the DOM to count meta tags, schema.org itemtypes, and OpenGraph properties, normalizing counts to a 0–1 range.
- **Example Metrics:** `structure = 0.73` when meta coverage, schema annotations, and social tags are balanced.

## SemanticAgent (`leo/agents/semantic_agent.py`)
- **Purpose:** Measure semantic coherence across the page body.
- **Inputs:** `state.text`
- **Outputs:** `state.metrics["semantic"]`
- **Logic:** Splits text into ~500 character chunks, calls `openai.embeddings.create` when an API key is available (falling back to deterministic embeddings), and averages pairwise cosine similarity.
- **Example Metrics:** `semantic = 0.81` for tightly aligned paragraphs.

## ScoringAgent (`leo/agents/scoring_agent.py`)
- **Purpose:** Compute the weighted LeoRank, capture retrieval readiness, and persist results.
- **Inputs:** `state.metrics`, `state.html`, `state.text`, pipeline `persist` flag.
- **Outputs:** `state.metrics["retrieval"]`, `state.leo_rank`, database entry in `scores` table.
- **Logic:** Loads weights from `leo/config/weights.yml`, calculates retrieval heuristics (text richness, heading density, link coverage), applies `LeoRank = 100 * (0.4·structure + 0.4·semantic + 0.2·retrieval)`, and inserts the score into SQLite/Postgres.
- **Example Metrics:** `retrieval = 0.58`, `LeoRank = 63.4` saved with the current timestamp.

## AdvisorAgent (`leo/agents/advisor_agent.py`)
- **Purpose:** Recommend actions that boost AI visibility.
- **Inputs:** `state.metrics`, `state.leo_rank`, environment `OPENAI_API_KEY`.
- **Outputs:** `state.suggestions`
- **Logic:** When an API key exists, sends a GPT chat completion seeded with the audit metrics; otherwise returns heuristic best practices.
- **Example Prompts:** GPT system message “You are an SEO assistant” plus URL, LeoRank, and metric summary.

# 📊 Scoring Formula
```
LeoRank = 100 * (0.4 * structure + 0.4 * semantic + 0.2 * retrieval)
```
Weights are stored in `leo/config/weights.yml` for easy adjustment.

# 🔍 LLM Interaction
- **SemanticAgent:** `openai.embeddings.create` generates paragraph vectors when `OPENAI_API_KEY` is present, with deterministic embeddings as a fallback.
- **AdvisorAgent:** Uses GPT chat completions (`gpt-4o-mini` by default) to craft optimization advice; reverts to static heuristics without credentials.

# ⚙️ Configuration & Deployment
- `charts/leo-core/values.yaml` exposes:
  - `env.OPENAI_API_KEY` for secret injection.
  - `db.engine`, `POSTGRES_ENABLED`, and Postgres connection settings.
  - `cronjob.schedule` and `cronjob.urls` to automate recurring audits.
  - `mcp.enabled` and `mcp.port` to toggle the MCP deployment.
- SQLite stores data at `/tmp/leo.db`; Postgres is activated via `POSTGRES_ENABLED=true` or chart values.
- CronJobs reuse the CLI to enqueue audits on schedule; MCP deployment offers GPT-native connectivity.

# 🧱 Future Extensions (v0.3 Placeholder)
- Kafka event streaming for real-time visibility updates.
- Rynions AI agents integration for collaborative remediation.
