"""
leo/graph.py
Defines the LangGraph-style pipeline orchestrating LEO Core agents.
Each agent reads and writes to a shared LeoState object.
"""

from leo.state import LeoState
from leo.agents.crawler_agent import CrawlerAgent
from leo.agents.structure_agent import StructureAgent
from leo.agents.semantic_agent import SemanticAgent
from leo.agents.scoring_agent import ScoringAgent
from leo.agents.advisor_agent import AdvisorAgent
from leo.db import save_score


def run_pipeline(url: str) -> LeoState:
    """
    Execute the full LEO pipeline:
    Crawler → Structure → Semantic → Scoring → Advisor.
    """
    state = LeoState(url=url)

    print(f"[LEO] Starting audit for: {url}")

    # 1️⃣ Crawler
    crawler = CrawlerAgent()
    state = crawler.run(state)
    print("[LEO] Crawler complete")

    # 2️⃣ Structure analysis
    structure = StructureAgent()
    state = structure.run(state)
    print("[LEO] Structure analysis complete")

    # 3️⃣ Semantic analysis
    semantic = SemanticAgent()
    state = semantic.run(state)
    print("[LEO] Semantic analysis complete")

    # 4️⃣ Scoring
    scorer = ScoringAgent()
    state = scorer.run(state)
    print(f"[LEO] Scoring complete — LeoRank: {state.leo_rank:.2f}")

    # 5️⃣ Advisor
    advisor = AdvisorAgent()
    state = advisor.run(state)
    print("[LEO] Advisor suggestions generated")

    # Save to DB
    if state.leo_rank is not None:
        save_score(state.url, state.leo_rank)

    print("[LEO] Audit finished successfully ✅")
    return state


if __name__ == "__main__":
    # Manual run (for local testing)
    result = run_pipeline("https://openai.com")
    print(result.model_dump_json(indent=2))
