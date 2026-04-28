from app.services.vector_store_service import vector_store


def load_initial_knowledge():
    docs = [
        "Tech companies are focusing on AI-driven growth and cloud expansion.",
        "Rising interest rates impact stock valuations negatively.",
        "Supply chain disruptions affect manufacturing companies.",
        "Strong earnings reports boost investor confidence.",
        "Regulatory risks impact fintech and banking sectors."
    ]

    metadatas = [{"source": "knowledge_base"} for _ in docs]
    vector_store.add_documents(docs, metadatas)


#  Call once at startup
load_initial_knowledge()


def retrieve_market_knowledge(company):
    query = f"{company} industry trends risks opportunities financial performance"

    results = vector_store.search(query, k=5)

    return "\n".join(results)