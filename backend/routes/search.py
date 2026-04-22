from fastapi import APIRouter, Query
from typing import Optional
from backend.repositories.SearchRepository import SearchRepository
from backend.services.SearchService import SearchService

router = APIRouter()
search_repo = SearchRepository(db_path="./data", collection_name="ecommerce_products")
search_service = SearchService(search_repo=search_repo)

@router.get("/search")
def search_products(
    # Zorunlu parametre
    query: str = Query(..., min_length=2, description="Kullanıcının girdiği arama metni"),
    
    # İsteğe bağlı filtre parametreleri
    category: Optional[str] = Query(None, description="Ana kategoriye göre filtrele"),
    max_price: Optional[float] = Query(None, description="Maksimum fiyat filtresi"),
    
    # Sayfalama / Limit
    limit: int = Query(10, description="Döndürülecek maksimum ürün sayısı", le=50)
):
    """
    Kullanıcının sorgusunu alır ve ChromaDB üzerinde Hibrit Arama (Semantik + Filtre) yapar.
    """
    
    # 2. Servisi Çağır (İş Kuralları ve Veritabanı Araması burada çalışır)
    products = search_service.search_with_filters(
        query=query,
        category_name=category,
        max_price=max_price,
        top_n=limit
    )

    # 3. Sonuçları Frontend'e uygun JSON formatında döndür
    return {
        "query": query,
        "active_filters": {
            "category": category,
            "max_price": max_price
        },
        "count": len(products),
        # Pydantic v2 kullanıyorsan .model_dump() standarttır. 
        # Eğer Pydantic v1 ise burayı tekrar [p.dict() for p in products] yapabilirsin.
        "data": [p.model_dump() for p in products] 
    }