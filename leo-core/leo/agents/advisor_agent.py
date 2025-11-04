"""
leo/agents/advisor_agent.py
Generates actionable recommendations based on structure, semantic, and LeoRank results.
If OpenAI API is available, enhances suggestions using GPT; otherwise uses static logic.
"""

import os
from leo.state import LeoState

try:
    import openai
except ImportError:
    openai = None


class AdvisorAgent:
    """Provide recommendations to improve AI visibility and LEO rank."""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        if self.api_key and openai:
            openai.api_key = self.api_key

    def _static_recommendations(self, state: LeoState):
        """Fallback static logic."""
        tips = []
        s = state.metrics.get("structure", 0)
        sem = state.metrics.get("semantic", 0)
        rank = state.leo_rank or 0

        if s < 60:
            tips.append("Add descriptive <alt> tags to images and ensure meta tags are unique.")
        if sem < 60:
            tips.append("Improve on-page text clarity and include relevant AI/tech keywords naturally.")
        if rank < 70:
            tips.append("Strengthen both content structure and readability for better AI comprehension.")
        if not tips:
            tips.append("Your site structure and semantic clarity are strong. Continue consistent updates.")

        return tips

    def run(self, state: LeoState) -> LeoState:
        print("[AdvisorAgent] Generating improvement suggestions...")

        if self.api_key and openai:
            try:
                prompt = f"""
                You are an AI visibility auditor.
                The website has these metrics:
                Structure: {state.metrics.get('structure')}
                Semantic: {state.metrics.get('semantic')}
                LeoRank: {state.leo_rank}

                Suggest 3 concise improvements to increase AI visibility.
                """
                chat = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200,
                )
                suggestions = [m["message"]["content"].strip() for m in chat.choices]
                print("[AdvisorAgent] ✅ Online GPT recommendations generated.")
            except Exception as e:
                print(f"[AdvisorAgent] ⚠️ OpenAI API failed ({e}) — using static recommendations.")
                suggestions = self._static_recommendations(state)
        else:
            suggestions = self._static_recommendations(state)
            print("[AdvisorAgent] ✅ Static recommendations applied.")

        state.suggestions = suggestions
        return state
