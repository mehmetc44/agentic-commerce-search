import chromadb
from typing import List, Generator
from backend.Models.Product import Product

class ProductRepository:
    def __init__(self, db_path: str = "./data", collection_name: str = "ecommerce_products"):
        """
        ChromaDB'den standart veri çekme ve listeleme işlemlerini yönetir.
        """
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_collection(name=collection_name)

    def get_all(self, chunksize: int = 1000) -> Generator[Product, None, None]:
        """
        Tüm ürünleri memory'i şişirmeden parça parça (offset ile) generator olarak döner.
        """
        offset = 0
        while True:
            # limit ve offset ile veritabanını yormadan verileri çekiyoruz
            results = self.collection.get(limit=chunksize, offset=offset)
            
            # Veri kalmadıysa döngüyü kır
            if not results or not results.get("metadatas") or len(results["metadatas"]) == 0:
                break
            
            for meta in results["metadatas"]:
                yield Product(**meta)
            
            offset += chunksize

    def get_paginated(self, page: int, page_size: int) -> List[Product]:
        """
        Sayfalama (Pagination) için offset ve limit kullanarak istenen sayfayı çeker.
        """
        offset = (page - 1) * page_size
        results = self.collection.get(limit=page_size, offset=offset)
        
        products = []
        if results and results.get("metadatas"):
            for meta in results["metadatas"]:
                products.append(Product(**meta))
                
        return products
        
    def get_by_id(self, parent_asin: str) -> Product | None:
        """
        Spesifik bir ürünü ID'sine (parent_asin) göre getirir.
        """
        results = self.collection.get(ids=[str(parent_asin)])
        
        if results and results.get("metadatas") and len(results["metadatas"]) > 0:
            return Product(**results["metadatas"][0])
        return None
    def get_by_filter(self, where_clause: Dict[str, Any], limit: int = 50, offset: int = 0) -> List[Product]:
        """
        ChromaDB'nin 'where' parametresini kullanarak veritabanı seviyesinde filtreleme yapar.
        """
        results = self.collection.get(
            where=where_clause,
            limit=limit,
            offset=offset
        )
        
        products = []
        if results and results.get("metadatas"):
            for meta in results["metadatas"]:
                products.append(Product(**meta))
                
        return products