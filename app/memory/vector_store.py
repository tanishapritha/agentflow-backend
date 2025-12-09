from typing import List, Dict, Any

class VectorStore:
    """
    Mock Vector Store.
    In production this would connect to Pinecone/Chroma.
    """
    def __init__(self):
        self.store = {}

    def add_documents(self, documents: List[str]):
        # Mock implementation
        pass

    def search(self, query: str) -> List[str]:
        # Mock implementation
        return ["Mock retrieved context based on query"]
