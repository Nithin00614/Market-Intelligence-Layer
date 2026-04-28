from langgraph.graph import StateGraph, END
from app.state import GraphState

from app.agents.news_agent import news_agent
from app.agents.financial_data_agent import financial_data_agent
from app.agents.analysis_agent import analysis_agent
from app.agents.strategy_agent import strategy_agent

#  NEW: Import vector store
from app.services.vector_store_service import vector_store


# -------------------------------
#  RAG WRAPPER (IMPORTANT)
# -------------------------------
def rag_analysis_agent(state: GraphState):

    company = state.get("company", "")

    #  Retrieve relevant knowledge
    retrieved_docs = vector_store.search(
        f"{company} industry trends risks opportunities",
        k=5
    )

    # filter by company file
    retrieved_docs = [doc for doc in retrieved_docs if company.lower() in doc["source"].lower()][:3]
    # Add to state
    state["knowledge"] = retrieved_docs

    # Call original analysis agent
    return analysis_agent(state)


# -------------------------------
# GRAPH BUILD
# -------------------------------
def build_graph():

    workflow = StateGraph(GraphState)

    # Nodes
    workflow.add_node("news", news_agent)
    workflow.add_node("finance", financial_data_agent)

    #  Replace analysis node with RAG-enabled one
    workflow.add_node("analysis", rag_analysis_agent)

    workflow.add_node("strategy", strategy_agent)

    # Flow
    workflow.set_entry_point("news")

    workflow.add_edge("news", "finance")
    workflow.add_edge("finance", "analysis")
    workflow.add_edge("analysis", "strategy")
    workflow.add_edge("strategy", END)

    return workflow.compile()