from repositories.category_repository import CategoryRepository

class CategoryService:
    def __init__(self):
        self.repository = CategoryRepository()

    def get_categories(self, limit: int = 100):
        return self.repository.get_all(limit=limit)

    def get_category(self, category_id: int):
        return self.repository.get_by_id(category_id)

    def get_main_categories(self, limit: int = 100):
        return self.repository.get_main_categories(limit)

    def get_closest_categories(self, vector: list[float], limit: int = 10):
        return self.repository.get_closest(vector, limit)
