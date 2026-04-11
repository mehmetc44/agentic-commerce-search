from tracemalloc import start
from typing import List, Optional, Generator
import pandas as pd
from backend.Models.Product import Product

class ProductRepository:
    def __init__(self, categories_path: str, products_path: str, chunksize: int = 10000):
        """
        Büyük CSV'ler için memory-efficient repository
        chunksize: Kaç satır bir seferde belleğe alınsın
        """
        self.categories_df = pd.read_csv(categories_path)
        self.products_path = products_path
        self.chunksize = chunksize

    def get_all(self) -> Generator[Product, None, None]:
        """
        Tüm ürünleri generator olarak döner, memory dostu
        """
        for chunk in pd.read_csv(self.products_path, chunksize=self.chunksize):
            for row in chunk.to_dict(orient="records"):
                yield Product(**row)
    def get_paginated(self, page: int, page_size: int):
        start = (page - 1) * page_size
        end = start + page_size

        index = 0

        for chunk in pd.read_csv(self.products_path, chunksize=self.chunksize):
            for row in chunk.to_dict(orient="records"):
                if index >= start and index < end:
                    yield Product(**row)

                if index >= end:
                    return

                index += 1
    def get_by(self, predicate):
        for chunk in pd.read_csv(self.products_path, chunksize=self.chunksize):
            for row in chunk.to_dict(orient="records"):
                product = Product(**row)
                if predicate(product):
                    yield product
    