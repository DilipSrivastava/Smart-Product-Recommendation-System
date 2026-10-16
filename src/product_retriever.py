from src.embedding_generator import EmbeddingGenerator
from src.vector_store import VectorStore


class ProductRetriever:

    def __init__(self):
        self.embedding_generator = EmbeddingGenerator()
        self.vector_store = VectorStore()

    def search(self, query, top_k=4):
        query_embedding = self.embedding_generator.generate_embedding(query)

        matches = self.vector_store.search(
            query_embedding,
            top_k=top_k
        )

        products = []

        for match in matches:
            products.append({
                "id": match.id,
                "name": match.metadata["name"],
                "category": match.metadata["category"],
                "price": float(match.metadata["price"]),
                "description": match.metadata["description"],
                "features": match.metadata["features"],
                "target_audience": match.metadata["target_audience"],
                "score": float(match.score)
            })

        return products