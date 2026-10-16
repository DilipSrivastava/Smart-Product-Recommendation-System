
from src.product_retriever import ProductRetriever

retriever = ProductRetriever()

query = "I need a laptop for Java development under 70000"

results = retriever.search(query, top_k=5)

for product in results:
    print(f"\nProduct: {product['name']}")
    print(f"Price: ₹{product['price']}")
    print(f"Category: {product['category']}")
    print(f"Similarity score: {product['score']:.4f}")
    print(f"Description: {product['description']}")
