from typing import TypedDict, List, Dict, Any

class GraphState(TypedDict, total=False):
    company: str
    news: List[Dict[str, Any]]
    financial_data: Dict[str, Any]
    analysis: Dict[str, Any]
    strategy: Dict[str, Any]