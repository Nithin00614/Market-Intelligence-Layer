from fastapi import FastAPI
from app.api.routes import router
from app.services.vector_store_service import VectorStore
import os

app = FastAPI()

app.include_router(router)

vector_store = VectorStore()

@app.on_event("startup")
def load_documents():

    docs = []

    for file in os.listdir("data/market_docs"):

        with open(f"data/market_docs/{file}") as f:
            docs.append(f.read())

    vector_store.add_documents(docs)
