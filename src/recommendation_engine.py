import json
from pathlib import Path

from src.product_retriever import ProductRetriever


class RecommendationEngine:

    def __init__(self):
        self.retriever = ProductRetriever()

        catalog_path = Path(__file__).resolve().parent.parent / "data" / "products.json"

        with open(catalog_path, "r", encoding="utf-8") as file:
            self.products = json.load(file)

    def recommend(self, query, max_price=None):
        query_lower = query.lower()

        laptop_request = (
            "laptop" in query_lower
            or "notebook computer" in query_lower
        )

        retrieved = self.retriever.search(query, top_k=10)
        retrieved_scores = {
            product["id"]: product["score"]
            for product in retrieved
        }

        eligible = []

        for product in self.products:
            name = product["name"].lower()
            category = product["category"].lower()
            price = float(product["price"])

            if max_price is not None and price > max_price:
                continue

            if laptop_request:
                if "laptop" not in name or "cooling pad" in name:
                    continue

            product = product.copy()
            product["price"] = price
            product["score"] = retrieved_scores.get(product["id"], 0.0)
            eligible.append(product)

        eligible.sort(
            key=lambda product: (
                product["score"],
                -product["price"]
            ),
            reverse=True
        )

        return {
            "main_product": eligible[0] if eligible else None,
            "recommendations": eligible[1:4]
        }