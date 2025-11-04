# Leo Core Architecture

```mermaid
graph LR
  A[Crawler] --> B[Structure]
  B --> C[Semantic]
  C --> D[Scoring]
  D --> E[Advisor]
  E --> F[(Database)]
```

The crawler ingests HTML which flows through structure, semantic, and scoring agents before the advisor produces recommendations and stores results in the configured database. The CLI, API, MCP server, and Helm deployments orchestrate this LangGraph pipeline for different surfaces.
