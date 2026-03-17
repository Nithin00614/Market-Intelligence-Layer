import faiss
from app.services.embedding_service import get_embeddings

class VectorStore:

    def __init__(self):

        self.index = faiss.IndexFlatL2(384)
        self.docs = []

    def add_documents(self, documents):

        embeddings = get_embeddings(documents)

        self.index.add(embeddings)

        self.docs.extend(documents)

    def search(self, query):

        if not self.docs:
            return []

        query_embedding = get_embeddings([query])

        _, I = self.index.search(query_embedding, 3)

        return [self.docs[i] for i in I[0] if i < len(self.docs)]