
from pinecone import Pinecone, ServerlessSpec
from src.config import PINECONE_API_KEY, PINECONE_INDEX_NAME


class VectorStore:

    def __init__(self):
        print("Connecting to Pinecone...")
        self.client = Pinecone(api_key=PINECONE_API_KEY)

        existing_indexes = self.client.list_indexes().names()

        if PINECONE_INDEX_NAME not in existing_indexes:
            self.client.create_index(
                name=PINECONE_INDEX_NAME,
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )

        self.index = self.client.Index(PINECONE_INDEX_NAME)

    def upsert_products(self, products):
        vectors = []

        for product in products:
            vectors.append({
                "id": product["id"],
                "values": product["embedding"],
                "metadata": {
                    "name": product["name"],
                    "category": product["category"],
                    "price": product["price"],
                    "description": product["description"],
                    "features": ", ".join(product["features"]),
                    "target_audience": product["target_audience"]
                }
            })

        for start in range(0, len(vectors), 100):
            self.index.upsert(
                vectors=vectors[start:start + 100]
            )

        print(f"Stored {len(vectors)} products in Pinecone.")

    def search(self, query_embedding, top_k=5):
        response = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )

        return response.matches
