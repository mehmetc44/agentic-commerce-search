"""
product_tools.py — LangGraph için ürün arama tool'u.

Sadece HTTP katmanı. Tüm AI işlemleri (embedding, cross-encoder)
catalog-api tarafında gerçekleşir.
"""

from langchain_core.tools import tool
import json
from typing import List, Optional
from clients.catalog_client import CatalogAPIClient

_client = CatalogAPIClient()


@tool
def list_closest_products(
    category_ids: List[str],
    product_query: str,
    brand: Optional[str] = None,
    color: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
) -> str:
    """
    Verilen kategori ID'lerinde ve filtrelerde en uygun ürünleri arar ve sıralar.

    Args:
        category_ids:  Ürünlerin aranacağı kategori ID'leri (Örn: ["101", "102"]).
        product_query: Anlamsal arama için sorgu cümlesi
                       (Örn: 'su geçirmez kışlık çadır').
        brand:         (Opsiyonel) Marka filtresi.
        color:         (Opsiyonel) Renk filtresi.
        min_price:     (Opsiyonel) Minimum fiyat (şu an kullanılmıyor).
        max_price:     (Opsiyonel) Maksimum fiyat (şu an kullanılmıyor).

    Returns:
        JSON string formatında önerilen ürünler listesi.
    """
    try:
        results = _client.search_products(
            query=product_query,
            category_ids=category_ids,
            brand=brand,
            color=color,
            max_results=10,
        )
        return json.dumps(results, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})
