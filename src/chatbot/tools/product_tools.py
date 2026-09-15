from langchain_core.tools import tool
import json
from typing import List, Optional
from chatbot.services.container import container

@tool
def list_closest_products(category_ids: List[str], product_query: str, brand: str = None, color: str = None, min_price: int = None, max_price: int = None) -> str:
    """
    Verilen kategori ID'lerinde ve hard filtrelerde (marka, renk, fiyat) ürünleri arar ve vektör benzerliğine göre sıralayıp getirir.
    
    Args:
        category_ids: Ürünlerin aranacağı kategori ID'leri listesi (Örn: ["101", "102"]).
        product_query: Vektör (anlamsal) arama için sorgu cümlesi (Örn: 'su geçirmez kışlık çadır').
        brand: (Opsiyonel) Kesin marka filtresi.
        color: (Opsiyonel) Kesin renk filtresi.
        min_price: (Opsiyonel) Minimum fiyat.
        max_price: (Opsiyonel) Maksimum fiyat.
        
    Returns:
        JSON string formatında önerilen ürünler listesi.
    """
    try:
        # Construct the filters dictionary expected by ProductSearchService
        extracted_filters = {
            "category_taxonomy": category_ids,
        }
        
        if brand: extracted_filters["brand"] = brand
        if color: extracted_filters["color"] = [color]
        if min_price: extracted_filters["min_price"] = min_price
        if max_price: extracted_filters["max_price"] = max_price
        
        final_json = {
            "analysis": {
                "rewritten_query": product_query,
                "extracted_filters": extracted_filters
            }
        }
        
        # We reuse the ProductSearchService from the legacy project!
        top_products = container.product_search.search_products(final_json=final_json, max_results=10)
        
        # Prepare for LLM response
        results = []
        for p in top_products:
            results.append({
                "product_id": p.get("product_id"),
                "title": p.get("title"),
                "price": 0, # Note: Price is generated dynamically in UI, or add actual DB price column later.
                "category_id": p.get("category_id"),
                "match_score": f"{p.get('cross_encoder_score', 0):.1f}%"
            })
            
        return json.dumps(results, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({"error": str(e)})
