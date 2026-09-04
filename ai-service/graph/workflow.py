from langgraph.graph import END, START, StateGraph

from graph.state import AnalysisState, create_initial_state
from graph.nodes import (
    weather_node,
    ocean_node,
    ecosystem_node,
    risk_node,
    decision_node,
    finalize_node,
)


def build_workflow():
    """
    Build the ORCA multi-agent LangGraph workflow.

    Flow:
        START
          ↓
        Weather
          ↓
        Ocean
          ↓
        Ecosystem
          ↓
        Risk
          ↓
        Decision
          ↓
        Finalize
          ↓
        END
    """

    graph = StateGraph(AnalysisState)

    graph.add_node("weather", weather_node)
    graph.add_node("ocean", ocean_node)
    graph.add_node("ecosystem", ecosystem_node)
    graph.add_node("risk", risk_node)
    graph.add_node("decision", decision_node)
    graph.add_node("finalize", finalize_node)

    graph.add_edge(START, "weather")
    graph.add_edge("weather", "ocean")
    graph.add_edge("ocean", "ecosystem")
    graph.add_edge("ecosystem", "risk")
    graph.add_edge("risk", "decision")
    graph.add_edge("decision", "finalize")
    graph.add_edge("finalize", END)

    return graph.compile()


# Compiled workflow used by the application.
marine_graph = build_workflow()


def run_analysis(request: dict) -> AnalysisState:
    """
    Execute the complete ORCA analysis workflow.

    Parameters
    ----------
    request:
        Validated analysis request represented as a dictionary.

    Returns
    -------
    AnalysisState
        Final graph state containing all agent results,
        zone decisions, errors and partial-state information.
    """

    initial_state = create_initial_state(request)

    result = marine_graph.invoke(initial_state)

    return result