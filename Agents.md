# === PROJECT INSTRUCTION ===
You are an AI engineer setting up version 0.1 of an open-source project called **Leo Core** —
the foundation for “AI Visibility Scoring (LeoRank)” using LangGraph agents.

Generate every file and folder listed below with working starter code.
All components must run locally (`python cli.py audit <url>`), via API (`uvicorn api.server:app`),
in Docker, and be deployable with Helm (`helm install leo-core charts/leo-core -n leo`).

-------------------------------------------------
📦  REPOSITORY STRUCTURE
-------------------------------------------------
leo-core/
├── leo/
│   ├── __init__.py
│   ├── state.py
│   ├── graph.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── crawler_agent.py
│   │   ├── structure_agent.py
│   │   ├── semantic_agent.py
│   │   ├── scoring_agent.py
│   │   └── advisor_agent.py
│   ├── utils/
│   │   ├── html_utils.py
│   │   ├── metrics_utils.py
│   │   └── report_utils.py
│   └── config/weights.yml
│
├── api/
│   ├── __init__.py
│   └── server.py
│
├── charts/leo-core/
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── .helmignore
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── ingress.yaml
│       ├── configmap.yaml
│       └── secret.yaml
│
├── cli.py
├── Dockerfile
├── requirements.txt
├── pyproject.toml
├── README.md
└── examples/sample_report.json

-------------------------------------------------
🧩  FILE REQUIREMENTS
-------------------------------------------------

## leo/state.py
Pydantic class `LeoState`:
- url: str  
- html: Optional[str]  
- text: Optional[str]  
- metrics: Dict[str, float]  
- leo_rank: Optional[float]  
- suggestions: List[str]

## leo/graph.py
Create LangGraph pipeline:
crawl → structure → semantic → score → advisor → END.

## agents
- crawler_agent.py → fetch HTML & extract text with BeautifulSoup.
- structure_agent.py → count meta/schema/og tags → normalized 0–1 score.
- semantic_agent.py → split text into 500-char chunks, embed with stub (no API yet),
  compute cosine similarity → `metrics["semantic"]`.
- scoring_agent.py → `leo_rank = round(100*(0.5*structure + 0.5*semantic),2)`.
- advisor_agent.py → dummy static suggestions (3 strings).

## cli.py
Use **Typer** CLI:
`leo audit <url>` runs the graph, prints and saves JSON report.

## api/server.py
FastAPI `/audit?url=` endpoint returning LeoRank JSON.

## requirements.txt
langgraph, typer, fastapi, uvicorn, requests, beautifulsoup4, pydantic, numpy, scikit-learn.

## Dockerfile
FROM python:3.11-slim  
WORKDIR /app  
COPY . .  
RUN pip install -r requirements.txt  
CMD ["uvicorn","api.server:app","--host","0.0.0.0","--port","8000"]

## charts/leo-core/Chart.yaml
apiVersion: v2  
name: leo-core  
description: Helm chart for Leo Core  
version: 0.1.0  
appVersion: 0.1.0

## charts/leo-core/values.yaml
replicaCount: 1  
image.repository: ghcr.io/leo-labs/leo-core  
image.tag: "0.1.0"  
service.port: 8000  
env.OPENAI_API_KEY: ""  
ingress.enabled: true  
ingress.className: nginx  
ingress.hosts[0].host: leo.local  
ingress.hosts[0].paths[0]: "/"

## templates/deployment.yaml
K8s Deployment mounting secret `leo-core-secrets`,
passing OPENAI_API_KEY env var, exposing port 8000.

## templates/service.yaml
ClusterIP Service on port 8000.

## templates/secret.yaml
Secret with key OPENAI_API_KEY from values.

## templates/ingress.yaml
Optional ingress enabled via values.

## README.md
Describe purpose, architecture, usage examples, and contribution guide.
Include:
1️⃣ `python cli.py audit https://openai.com`
2️⃣ `docker build -t leo-core:0.1.0 .`
3️⃣ `helm install leo-core charts/leo-core -n leo`

-------------------------------------------------
✅  EXPECTED BEHAVIOR
-------------------------------------------------
- Running CLI prints JSON with dummy LeoRank (0–100).
- API endpoint `/audit?url=` returns same JSON.
- Docker container serves API on :8000.
- Helm templates lint cleanly (`helm lint charts/leo-core` passes).

# === END OF INSTRUCTION ===
