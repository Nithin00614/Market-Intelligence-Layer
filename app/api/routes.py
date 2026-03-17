from fastapi import APIRouter
from app.schemas.request_schema import MarketRequest
from app.workflows.agent_graph import build_graph

router = APIRouter()

graph = build_graph()


@router.post("/analyze-market")

def analyze_market(request: MarketRequest):

    state = {
        "company": request.company
    }

    result = graph.invoke(state)

    return result