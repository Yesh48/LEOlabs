from leo.state import LeoState
from leo.agents.structure_agent import StructureAgent

def test_structure_score_present():
    html = "<html><head><meta><title>T</title></head><body><h1>H</h1><img src='a.jpg' alt='x'><a href='/'>x</a></body></html>"
    s = LeoState(url="https://x.com", html=html)
    s = StructureAgent().run(s)
    assert "structure" in s.metrics
