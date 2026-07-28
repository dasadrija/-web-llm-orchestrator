import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class SimpleRAGPipeline:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.encoder = SentenceTransformer(model_name)
        self.index = None
        self.documents = []

    def add_documents(self, docs: list[str]):
        self.documents.extend(docs)
        embeddings = self.encoder.encode(docs, convert_to_numpy=True)
        dimension = embeddings.shape[1]
        
        if self.index is None:
            self.index = faiss.IndexFlatL2(dimension)
        
        self.index.add(embeddings)

    def search(self, query: str, k: int = 2) -> list[str]:
        if not self.documents or self.index is None:
            return []
        query_vector = self.encoder.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_vector, k)
        
        results = []
        for idx in indices[0]:
            if idx < len(self.documents) and idx != -1:
                results.append(self.documents[idx])
        return results
