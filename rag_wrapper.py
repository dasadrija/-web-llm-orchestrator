from src.wrapper import ProductionLLMWrapper
from src.rag import SimpleRAGPipeline

class RAGWebsiteWrapper(ProductionLLMWrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rag = SimpleRAGPipeline()

    def query_with_context(self, user_message: str) -> str:
        relevant_docs = self.rag.search(user_message, k=2)
        context_str = "\n".join(relevant_docs) if relevant_docs else "No specific document context found."
        
        enhanced_prompt = f"Reference Context:\n{context_str}\n\nUser Question: {user_message}"
        return self.query(enhanced_prompt)
