from repositories.product_repository import ProductRepository

class ProductService:
    def __init__(self):
        self.repository = ProductRepository()

    def get_products(self, limit: int = 100):
        return self.repository.get_all(limit=limit)

    def get_product(self, product_id: int):
        return self.repository.get_by_id(product_id)
