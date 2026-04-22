from typing import List, Optional
from backend.repositories.SearchRepository import SearchRepository
from backend.Models.Product import Product

class SearchService:
    def __init__(self, search_repo: SearchRepository):
        self.search_repo = search_repo

    def basic_search(self, query: str, top_n: int = 10) -> List[Product]:
        """
        Sadece serbest metin ile düz semantik arama yapar.
        Örnek: "plajda giymelik rahat şeyler"
        """
        # Kullanıcıdan gelen girdiyi temizle (boşlukları sil, küçült vb.)
        clean_query = query.strip().lower()
        
        # Gerekirse burada query, mimari zeka katmanından geçirilerek genişletilebilir 
        # (Örn: "rahat şeyler" -> "rahat kıyafetler, pamuklu, oversize" gibi)
        
        return self.search_repo.search_similarity(query=clean_query, top_n=top_n)

    def search_with_filters(self, query: str, category_name: Optional[str] = None, max_price: Optional[float] = None, top_n: int = 10) -> List[Product]:
        """
        Semantik aramayı, kesin veritabanı filtreleriyle birleştirir (Hibrit Arama).
        Kullanıcı hem arama yapıp hem de sol menüden filtre seçtiğinde bu çalışır.
        """
        clean_query = query.strip().lower()
        
        # Filtre sözlüğünü dinamik olarak oluştur
        filters = []
        
        if category_name:
            filters.append({"main_category": category_name})
            
        if max_price is not None:
            filters.append({"price": {"$lt": max_price}})

        # ChromaDB where parametresi formatını ayarla
        where_clause = None
        if len(filters) == 1:
            where_clause = filters[0]
        elif len(filters) > 1:
            where_clause = {"$and": filters}

        return self.search_repo.search_similarity(
            query=clean_query, 
            top_n=top_n, 
            where_filter=where_clause
        )