from typing import TypedDict
from langgraph.graph import StateGraph, END

from app.agents.coordinator_agent import coordinator_agent
from app.agents.news_agent import news_agent
from app.agents.financial_data_agent import financial_data_agent
from app.agents.analysis_agent import analysis_agent
from app.agents.strategy_agent import strategy_agent


class AgentState(TypedDict, total=False):
    company: str
    tool_plan: str
    news: list
    financial_data: dict
    analysis: str
    final_report: str

def route_tools(state):

    plan = state.get("tool_plan", "")

    if "news_agent" in plan and "financial_agent" in plan:
        return "news_agent"

    if "news_agent" in plan:
        return "news_agent"

    if "financial_agent" in plan:
        return "financial_agent"

    return "analysis_agent"

def build_graph():

    workflow = StateGraph(AgentState)

    workflow.add_node("coordinator", coordinator_agent)
    workflow.add_node("news_agent", news_agent)
    workflow.add_node("financial_agent", financial_data_agent)
    workflow.add_node("analysis_agent", analysis_agent)
    workflow.add_node("strategy_agent", strategy_agent)

    workflow.set_entry_point("coordinator")

    workflow.add_conditional_edges(
        "coordinator",
        route_tools
    )

    workflow.add_edge("news_agent", "analysis_agent")
    workflow.add_edge("financial_agent", "analysis_agent")

    workflow.add_edge("analysis_agent", "strategy_agent")

    workflow.add_edge("strategy_agent", END)

    return workflow.compile()