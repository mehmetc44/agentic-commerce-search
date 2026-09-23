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
        if min_price and item["price"] < min_price:
            continue
        if max_price and item["price"] > max_price:
            continue
        if query:
            query_words = set(query.lower().split())
            item_words = set(item["name"].lower().split())
            # Basit bir kelime eşleştirme (en az 1 kelime tutuyorsa getir)
            # Daha iyisi: kelimelerin köklerine veya substringlerine bakmak.
            # Şimdilik: query içindeki kelimelerin bir kısmı name içinde var mı diye daha esnek bakalım
            match_found = False
            for q_word in query_words:
                if len(q_word) > 2 and any(q_word in i_word for i_word in item_words):
                    match_found = True
                    break
            if not match_found:
                continue
                
        results.append(item)
        
    if not results:
        return "Veritabanında uygun ürün bulunamadı."
        
    return f"Veritabanı Sonuçları: {json.dumps(results, ensure_ascii=False)}"
