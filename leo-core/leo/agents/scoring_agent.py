"""
leo/agents/scoring_agent.py
Aggregates structure, semantic, and other metrics into a single LEO Rank (0–100).
"""

import yaml
import os
from leo.state import LeoState


class ScoringAgent:
    """Combine weighted metrics to compute the final LeoRank score."""

    def __init__(self, weights_path: str = None):
        # Load weights from config
        default_path = weights_path or os.path.join(os.path.dirname(__file__), "..", "config", "weights.yml")
        if os.path.exists(default_path):
            with open(default_path, "r") as f:
                self.weights = yaml.safe_load(f).get("weights", {})
        else:
            self.weights = {"structure": 0.5, "semantic": 0.5}

    def run(self, state: LeoState) -> LeoState:
        print("[ScoringAgent] Computing LeoRank...")

        structure = state.metrics.get("structure", 0.0)
        semantic = state.metrics.get("semantic", 0.0)

        w_structure = self.weights.get("structure", 0.5)
        w_semantic = self.weights.get("semantic", 0.5)

        # Normalize total weights
        total_weight = w_structure + w_semantic or 1
        w_structure /= total_weight
        w_semantic /= total_weight

        leo_rank = (structure * w_structure + semantic * w_semantic)
        state.leo_rank = round(leo_rank, 2)

        print(f"[ScoringAgent] ✅ LeoRank computed: {state.leo_rank}")
        return state
