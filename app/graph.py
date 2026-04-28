from langgraph.graph import StateGraph, END
from app.state import GraphState

from app.agents.news_agent import news_agent
from app.agents.financial_data_agent import financial_data_agent
from app.agents.analysis_agent import analysis_agent
from app.agents.strategy_agent import strategy_agent


def build_graph():

    graph = StateGraph(GraphState)

    # Add nodes
    graph.add_node("news", news_agent)
    graph.add_node("finance", financial_data_agent)
    graph.add_node("analysis", analysis_agent)
    graph.add_node("strategy", strategy_agent)

    # Define flow
    graph.set_entry_point("news")

    graph.add_edge("news", "finance")
    graph.add_edge("finance", "analysis")
    graph.add_edge("analysis", "strategy")
    graph.add_edge("strategy", END)

    return graph.compile()