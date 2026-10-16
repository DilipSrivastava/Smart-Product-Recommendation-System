
import json
from pathlib import Path

from src.embedding_generator import EmbeddingGenerator
from src.vector_store import VectorStore


def main():
    catalog_path = Path("data/products.json")

    with catalog_path.open("r", encoding="utf-8") as file:
        products = json.load(file)

    print(f"Loaded {len(products)} products.")

    embedding_generator = EmbeddingGenerator()
    products = embedding_generator.generate_embeddings(products)

    vector_store = VectorStore()
    vector_store.upsert_products(products)

    print("Product catalog successfully loaded into Pinecone.")


if __name__ == "__main__":
    main()
