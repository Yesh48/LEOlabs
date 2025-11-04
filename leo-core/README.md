# 🦁 LEO Core — AI Visibility Scoring Engine

LEO Core analyzes any website for its **AI-visibility** — how clearly large language models can interpret, summarize, and rank its content.  
It’s like **SEO for LLMs** — evaluating structure, semantics, and clarity.

---

## 🚀 Features
- LangGraph pipeline with 5 agents:
  - **Crawler → Structure → Semantic → Scoring → Advisor**
- FastAPI microservice + Typer CLI
- SQLite / Postgres storage
- MCP server for GPT-native access
- Helm chart (Kubernetes) & Homebrew (macOS)
- CronJob for daily audits

---

## 🧩 Quick Start (Local)

```bash
git clone https://github.com/Yesh48/LEOlabs.git
cd LEOlabs/leo-core
pip install -r requirements.txt
export OPENAI_API_KEY="sk-..."
python cli.py audit https://openai.com
Or start API:

python cli.py serve
Then visit: http://127.0.0.1:8000/docs

☸️ Deploy with Helm
helm install leo-core charts/leo-core \
  -n leo --create-namespace \
  --set env.OPENAI_API_KEY="sk-..." \
  --set mcp.enabled=true
🍺 macOS Installation
brew tap yesh48/leo
brew install leo-core
leo audit https://openai.com
🧠 Agent Flow
graph LR
    A[CrawlerAgent] --> B[StructureAgent]
    B --> C[SemanticAgent]
    C --> D[ScoringAgent]
    D --> E[AdvisorAgent]
    E --> F[(DB)]
📊 Example Output
{
  "url": "https://openai.com",
  "metrics": {"structure": 79.2, "semantic": 82.4},
  "leo_rank": 80.8,
  "suggestions": [
    "Improve meta descriptions for clarity.",
    "Add structured data for FAQs."
  ],
  "timestamp": "2025-11-03T20:55:00Z"
}
🧩 MCP Integration
GPT models can call:

leo_audit(url: str) → full audit

leo_recent() → last 10 results

🤝 Contributing
Fork repo & create a feature branch

Run tests with pytest

Submit PRs with descriptive commits

📜 License
MIT © 2025 [Tekyantra Inc.]
