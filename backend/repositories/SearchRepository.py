import chromadb
from typing import List
from backend.Models.Product import Product

class SearchRepository:
    def __init__(self, db_path: str = "./data", collection_name: str = "ecommerce_products"):
        """
        Sadece semantik arama (Semantic Search) operasyonlarını yönetir.
        """
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_collection(name=collection_name)

    # backend/repositories/SearchRepository.py içerisindeki metot güncellemesi:

    def search_similarity(self, query: str, top_n: int = 10, where_filter: dict = None) -> List[Product]:
        """
        Anlamsal arama yaparken aynı zamanda ChromaDB'nin veritabanı seviyesindeki 
        filtrelerini (where) kullanarak sonuçları daraltır.
        """
        # where_filter None ise ChromaDB'ye bu parametreyi hiç göndermemeliyiz
        kwargs = {
            "query_texts": [query],
            "n_results": top_n
        }
        if where_filter:
            kwargs["where"] = where_filter

        results = self.collection.query(**kwargs)
        
        products = []
        if results and results.get("metadatas") and len(results["metadatas"]) > 0:
            for meta in results["metadatas"][0]:
                if meta:
                    products.append(Product(**meta))
                    
        return products