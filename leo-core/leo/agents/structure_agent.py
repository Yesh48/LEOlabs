"""
leo/agents/structure_agent.py
Analyzes HTML structure quality — headings, metadata, alt text, and links.
Produces a structure score (0–100).
"""

from bs4 import BeautifulSoup
from leo.state import LeoState


class StructureAgent:
    """Analyze the structural health of the website."""

    def run(self, state: LeoState) -> LeoState:
        if not state.html:
            print("[StructureAgent] ⚠️ No HTML found — skipping structural analysis.")
            state.metrics["structure"] = 0.0
            return state

        print("[StructureAgent] Analyzing HTML structure...")
        soup = BeautifulSoup(state.html, "html.parser")

        # Core structural elements
        headings = len(soup.find_all(["h1", "h2", "h3"]))
        metas = len(soup.find_all("meta"))
        images = soup.find_all("img")
        links = soup.find_all("a", href=True)

        # Quality checks
        alt_missing = sum(1 for img in images if not img.get("alt"))
        link_broken = sum(1 for a in links if not a["href"] or a["href"].startswith("#"))

        total_images = len(images) or 1
        total_links = len(links) or 1

        alt_ratio = (total_images - alt_missing) / total_images
        link_ratio = (total_links - link_broken) / total_links

        # Simple weighted score
        score = (
            (min(headings, 10) / 10) * 0.25 +
            (min(metas, 15) / 15) * 0.25 +
            alt_ratio * 0.25 +
            link_ratio * 0.25
        ) * 100

        state.metrics["structure"] = round(score, 2)
        print(f"[StructureAgent] ✅ Structure score: {state.metrics['structure']}")
        return state
