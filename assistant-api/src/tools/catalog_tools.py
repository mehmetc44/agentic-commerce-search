import requests
from langchain_core.tools import tool
from rag.embedder import embedder
from core.config import settings

@tool
def get_closest_categories(query: str, limit: int = 5) -> list[dict]:
    """Kullanıcının aramasına en uygun kategorileri veritabanından bulur.
    LLM bu aracı kullanarak arama cümlesini verir. Bu araç cümleyi vektöre çevirip veritabanında arar.
    """
    try:
        # 1. LLM'den gelen metni Vektöre çevir (assistant-api içinde yapılıyor)
        vector = embedder.embed_query(query)
        
        # 2. Vektörü catalog-api'ye gönderip en benzer kategorileri al
        url = f"{settings.CATALOG_API_URL}/api/categories/search-by-vector"
        
        # catalog-api'nin beklediği payload formatı (bunu catalog-api tarafında yazacaksın)
        payload = {
            "vector": vector,
            "limit": limit
        }
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            return [{"error": f"Kategoriler getirilemedi. Status: {response.status_code}"}]
            
    except Exception as e:
        return [{"error": f"Bir hata oluştu: {str(e)}"}]

@tool
def list_closest_products(category_id: int, query: str, limit: int = 5) -> list[dict]:
    """Belirli bir kategorideki en uygun ürünleri listeler."""
    # TODO: MCP veya catalog-api üzerinden doldurulacak
    raise NotImplementedError("Henüz implement edilmedi")

@tool
def get_category_filters(category_id: int) -> dict:
    """Kategoriye ait dinamik filtreleri (renk, beden, marka vb.) getirir."""
    # TODO: MCP veya catalog-api üzerinden doldurulacak
    raise NotImplementedError("Henüz implement edilmedi")
