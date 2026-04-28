import faiss
import numpy as np
import pickle
import os
from app.services.embedding_service import get_embeddings


# -------------------------------
# PATHS FOR PERSISTENCE
# -------------------------------
FAISS_INDEX_PATH = "faiss_index.bin"
METADATA_PATH = "metadata.pkl"


class VectorStore:
    def __init__(self):
        self.index = None
        self.docs = []
        self.metadatas = []

        #  Load existing index if available
        self._load_index()


    # -------------------------------
    # ADD DOCUMENTS (WITH METADATA)
    # -------------------------------
    def add_documents(self, documents, metadatas):
        if not documents:
            return

        embeddings = get_embeddings(documents)
        embeddings = np.array(embeddings).astype("float32")

        # Initialize index if not exists
        if self.index is None:
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)

        self.index.add(embeddings)
        self.docs.extend(documents)
        self.metadatas.extend(metadatas)

        #  Save after adding
        self._save_index()


    # -------------------------------
    # SEARCH FUNCTION (RAG CORE)
    # -------------------------------
    def search(self, query, k=5):
        if self.index is None or not self.docs:
            return []

        query_embedding = get_embeddings([query])
        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.index.search(query_embedding, k)

        results = []
        for i in indices[0]:
            if i < len(self.metadatas):
                results.append({
                    "text": self.docs[i],
                    "source": self.metadatas[i]["source"]
                })

        return results


    # -------------------------------
    # SAVE INDEX
    # -------------------------------
    def _save_index(self):
        if self.index is not None:
            faiss.write_index(self.index, FAISS_INDEX_PATH)

            with open(METADATA_PATH, "wb") as f:
                pickle.dump({
                    "docs": self.docs,
                    "metadatas": self.metadatas
                }, f)


    # -------------------------------
    # LOAD INDEX
    # -------------------------------
    def _load_index(self):
        if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(METADATA_PATH):
            try:
                self.index = faiss.read_index(FAISS_INDEX_PATH)

                with open(METADATA_PATH, "rb") as f:
                    data = pickle.load(f)

                self.docs = data.get("docs", [])
                self.metadatas = data.get("metadatas", [])

                print(f" Loaded FAISS index with {len(self.docs)} documents")

            except Exception as e:
                print(" Failed to load FAISS index:", str(e))
                self.index = None
                self.docs = []
                self.metadatas = []


# -------------------------------
# SINGLE GLOBAL INSTANCE
# -------------------------------
vector_store = VectorStore()