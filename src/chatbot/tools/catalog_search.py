from langchain_core.tools import tool
import json

@tool
def catalog_search_tool(category: str, min_price: float = None, max_price: float = None, query: str = None) -> str:
    """
    Mağazanın kendi ürün veritabanında arama yapar. Müşteriye ürün önermek için YALNIZCA bu araç kullanılmalıdır.
    """
    # Bu aşamada simülasyon (mock) verisi döndürüyoruz.
    # Gelecekte pgvector/SQL bağlantısı buraya eklenecektir.
    
    mock_db = [
        {"id": 1, "name": "Newholland Uyumlu LED Tepe Lambası 12V", "category": "Traktör Aksesuarları", "price": 1200.0, "stock": True},
        {"id": 2, "name": "Siyah Su Geçirmez Kışlık Bot", "category": "Ayakkabı", "price": 2500.0, "stock": True},
        {"id": 3, "name": "Mavi Su Geçirmez Çadır", "category": "Kamp", "price": 4500.0, "stock": False},
        {"id": 4, "name": "Erkek Spor Ayakkabı Siyah", "category": "Ayakkabı", "price": 1800.0, "stock": True},
        {"id": 5, "name": "Araba İçi LED Aydınlatma", "category": "Otomobil Aksesuar", "price": 850.0, "stock": True},
        {"id": 6, "name": "Oto Koltuk Kılıfı Siyah", "category": "Otomobil Aksesuar", "price": 1950.0, "stock": True}
    ]
    
    results = []
    for item in mock_db:
        if category and category.lower() not in item["category"].lower():
            continue
        if min_price and item["price"] < min_price:
            continue
        if max_price and item["price"] > max_price:
            continue
        if query and query.lower() not in item["name"].lower():
            continue
        results.append(item)
        
    if not results:
        return "Veritabanında uygun ürün bulunamadı."
        
    return f"Veritabanı Sonuçları: {json.dumps(results, ensure_ascii=False)}"
