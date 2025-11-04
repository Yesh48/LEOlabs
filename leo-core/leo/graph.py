"""LangGraph pipeline wiring for Leo Core."""
from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, StateGraph

from .agents import advisor_agent, crawler_agent, scoring_agent, semantic_agent, structure_agent
from .state import LeoState


class GraphState(TypedDict, total=False):
    leo_state: LeoState
    persist: bool


def _passthrough(state: GraphState, leo_state: LeoState) -> GraphState:
    return {"leo_state": leo_state, "persist": state.get("persist", True)}


def _crawler_node(state: GraphState) -> GraphState:
    leo_state = crawler_agent.run(state["leo_state"])
    return _passthrough(state, leo_state)


def _structure_node(state: GraphState) -> GraphState:
    leo_state = structure_agent.run(state["leo_state"])
    return _passthrough(state, leo_state)


def _semantic_node(state: GraphState) -> GraphState:
    leo_state = semantic_agent.run(state["leo_state"])
    return _passthrough(state, leo_state)


def _scoring_node(state: GraphState) -> GraphState:
    leo_state = scoring_agent.run(state["leo_state"], persist=state.get("persist", True))
    return _passthrough(state, leo_state)


def _advisor_node(state: GraphState) -> GraphState:
    leo_state = advisor_agent.run(state["leo_state"])
    return _passthrough(state, leo_state)


def build_graph() -> StateGraph:
    """Create the Leo pipeline graph."""
    workflow = StateGraph(GraphState)
    workflow.add_node("crawl", _crawler_node)
    workflow.add_node("structure", _structure_node)
    workflow.add_node("semantic", _semantic_node)
    workflow.add_node("score", _scoring_node)
    workflow.add_node("advisor", _advisor_node)

    workflow.set_entry_point("crawl")
    workflow.add_edge("crawl", "structure")
    workflow.add_edge("structure", "semantic")
    workflow.add_edge("semantic", "score")
    workflow.add_edge("score", "advisor")
    workflow.add_edge("advisor", END)

    return workflow


def get_compiled_graph():
    """Return a compiled LangGraph instance ready for execution."""
    return build_graph().compile()


def run_graph(url: str, persist: bool = True) -> LeoState:
    """Execute the Leo pipeline for a URL and return the final state."""
    graph = get_compiled_graph()
    initial_state: GraphState = {"leo_state": LeoState(url=url), "persist": persist}
    result: GraphState = graph.invoke(initial_state)
    return result["leo_state"]


def run_pipeline(url: str, persist: bool = True) -> LeoState:
    """Public helper mirroring the LangGraph pipeline invocation."""
    return run_graph(url, persist=persist)


def run_audit(url: str, persist: bool = True) -> LeoState:
    """Backwards compatible alias for the pipeline execution."""
    return run_pipeline(url, persist=persist)


__all__ = [
    "build_graph",
    "get_compiled_graph",
    "run_graph",
    "run_pipeline",
    "run_audit",
    "GraphState",
]
