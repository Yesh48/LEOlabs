"""
leo/agents/semantic_agent.py
Analyzes semantic quality of visible text — readability, relevance, and
embedding similarity if OpenAI API is available.
"""

import os
import re
import numpy as np
from leo.state import LeoState

try:
    import openai
except ImportError:
    openai = None


class SemanticAgent:
    """Evaluate text clarity, keyword density, and semantic cohesion."""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        if self.api_key and openai:
            openai.api_key = self.api_key

    def _fallback_score(self, text: str) -> float:
        """Offline stub for environments without API key."""
        words = text.split()
        avg_word_len = np.mean([len(w) for w in words]) if words else 0
        keyword_density = len(re.findall(r"(ai|ml|data|cloud|intelligence|automation)", text.lower()))
        # normalize
        score = min((avg_word_len * 5 + keyword_density * 10), 100)
        return round(score, 2)

    def run(self, state: LeoState) -> LeoState:
        if not state.text:
            print("[SemanticAgent] ⚠️ No text to analyze — skipping semantic stage.")
            state.metrics["semantic"] = 0.0
            return state

        print("[SemanticAgent] Analyzing semantic content...")

        # If API key exists, attempt embeddings
        if self.api_key and openai:
            try:
                chunks = state.text[:4000]  # limit to fit model context
                emb = openai.embeddings.create(input=chunks, model="text-embedding-3-small")
                vector = np.array(emb.data[0].embedding)
                cohesion = np.mean(vector[:128]) * 100
                score = max(0.0, min(cohesion, 100))
                print(f"[SemanticAgent] ✅ Online embedding analysis done. Score: {score:.2f}")
            except Exception as e:
                print(f"[SemanticAgent] ⚠️ OpenAI API failed — fallback mode ({e})")
                score = self._fallback_score(state.text)
        else:
            score = self._fallback_score(state.text)
            print(f"[SemanticAgent] ✅ Offline mode semantic score: {score}")

        state.metrics["semantic"] = score
        return state
