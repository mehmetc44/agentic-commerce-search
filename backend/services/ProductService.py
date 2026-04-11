from typing import Generator
from backend.Models.Product import Product
from backend.repositories.ProductRepository import ProductRepository

class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def get_paginated(self, page: int = 1, page_size: int = 40):
        return self.repo.get_paginated(page, page_size)

    def get_by_category(self, category_id: int):
        return self.repo.get_by(lambda p: p.category_id == category_id)

    def get_by_price_less_than(self, price: float):
        return self.repo.get_by(lambda p: p.price < price)

    def get_by_category_and_price(self, category_id: int, price: float):
        return self.repo.get_by(
            lambda p: p.category_id == category_id and p.price < price
        )