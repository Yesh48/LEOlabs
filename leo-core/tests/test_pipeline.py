from leo.state import LeoState
from leo.agents.scoring_agent import ScoringAgent

def test_scoring_computes_rank():
    s = LeoState(url="https://example.com", metrics={"structure": 80.0, "semantic": 60.0})
    s = ScoringAgent().run(s)
    assert 0 <= s.leo_rank <= 100
