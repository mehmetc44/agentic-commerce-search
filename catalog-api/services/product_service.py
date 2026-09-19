from repositories.product_repository import ProductRepository
from repositories.category_repository import CategoryRepository

class ProductService:
    def __init__(self):
        self.repository = ProductRepository()
        self.category_repository = CategoryRepository()

    def get_products(self, limit: int = 100):
        return self.repository.get_all(limit=limit)

    def get_product(self, product_id: int):
        return self.repository.get_by_id(product_id)

    def get_products_by_category(self, category_id: int, limit: int = 100):
        return self.repository.get_by_category_id(category_id, limit)

    def get_products_by_main_category(self, category_id: int, limit: int = 100):
        category = self.category_repository.get_by_id(category_id)
        if not category:
            return []
        
        main_category_path = category.get("full_path")
        return self.repository.get_by_main_category(main_category_path, limit)
