
from openai import OpenAI
from src.config import OPENAI_API_KEY


class EmbeddingGenerator:

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = "text-embedding-3-large"
        self.dimensions = 1536

    def generate_embedding(self, text):
        response = self.client.embeddings.create(
            model=self.model,
            input=text,
            dimensions=self.dimensions
        )

        return response.data[0].embedding

    def generate_embeddings(self, products):
        texts = []

        for product in products:
            text = (
                f"Product: {product['name']}\n"
                f"Category: {product['category']}\n"
                f"Description: {product['description']}\n"
                f"Features: {', '.join(product['features'])}\n"
                f"Target audience: {product['target_audience']}"
            )
            texts.append(text)

        if not texts:
            return products

        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
            dimensions=self.dimensions
        )

        for product, item in zip(products, response.data):
            product["embedding"] = item.embedding

        print(f"Generated embeddings for {len(products)} products.")

        return products
