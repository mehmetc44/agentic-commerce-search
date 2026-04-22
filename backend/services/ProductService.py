from typing import List
from backend.repositories.ProductRepository import ProductRepository
from backend.Models.Product import Product

class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def get_paginated(self, page: int = 1, page_size: int = 40) -> List[Product]:
        return self.repo.get_paginated(page, page_size)

    def get_by_category(self, category_name: str, limit: int = 40) -> List[Product]:
        """
        Belirli bir kategoriye ait ürünleri getirir.
        """
        # ChromaDB'de doğrudan eşitlik kontrolü
        where_filter = {"main_category": category_name} 
        return self.repo.get_by_filter(where_clause=where_filter, limit=limit)

    def get_by_price_less_than(self, price: float, limit: int = 40) -> List[Product]:
        """
        Fiyatı belirli bir değerden küçük olan ürünleri getirir.
        """
        # ChromaDB'de küçüktür ($lt - less than) operatörü kullanımı
        where_filter = {"price": {"$lt": price}}
        return self.repo.get_by_filter(where_clause=where_filter, limit=limit)

    def get_by_category_and_price(self, category_name: str, price: float, limit: int = 40) -> List[Product]:
        """
        Hem kategoriye uyan hem de fiyatı belirli bir değerin altında olan ürünleri getirir.
        """
        # Birden fazla koşul için ChromaDB'nin $and operatörü kullanılır
        where_filter = {
            "$and": [
                {"main_category": category_name},
                {"price": {"$lt": price}}
            ]
        }
        return self.repo.get_by_filter(where_clause=where_filter, limit=limit)