from agents.concept_agent import ConceptAgent
from agents.json_formatter_agent import JsonFormatterAgent
from backend.repositories.ProductRepository import ProductRepository
from backend.services.ProductService import ProductService

class ProductPipeline:
    def __init__(self, categories_path: str, products_path: str):
        self.repo = ProductRepository(categories_path, products_path)
        self.service = ProductService(self.repo)
        self.concept_agent = ConceptAgent()
        self.formatter_agent = JsonFormatterAgent()

    def run(self, user_prompt: str):
        # 1️⃣ Concept extraction
        concepts = self.concept_agent.generate_concepts(user_prompt)

        # 2️⃣ JSON formatting
        json_data = self.formatter_agent.format_to_json(concepts, metadata={})

        # 3️⃣ Early exit kontrolü
        if not json_data.get("is_query_valid", True):
            return {"error": json_data.get("clarification_message", "Invalid query")}

        # 4️⃣ Pre-filtering - şimdilik örnek: category=gift ve stock>0
        filtered_products = []
        for concept in json_data.get("expanded_semantic_queries", []):
            for product in self.repo.get_all():
                if concept.lower() in product.title.lower():
                    filtered_products.append(product)

        # 5️⃣ Top-K - max 10 ürün
        top_k = filtered_products[:10]

        return top_k