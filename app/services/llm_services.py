from langchain_groq import ChatGroq
from app.config.settings import settings

def get_llm():

    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.MODEL_NAME,
        temperature=0
    )

    return llm