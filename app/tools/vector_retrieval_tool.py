from app.services.vector_store_service import VectorStore

vector_store = VectorStore()

def retrieve_market_knowledge(company):

    query = f"market analysis of {company}"

    results = vector_store.search(query)

    return results