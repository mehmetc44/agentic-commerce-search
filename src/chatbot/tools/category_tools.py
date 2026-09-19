"""
category_tools.py — LangGraph için kategori arama tool'ları.

Sadece HTTP katmanı. Tüm AI işlemleri (embedding, cross-encoder)
catalog-api tarafında gerçekleşir.
"""

from langchain_core.tools import tool
import json
from chatbot.clients.catalog_client import CatalogAPIClient

_client = CatalogAPIClient()


@tool
def get_closest_categories(sample_query: str) -> str:
    """
    Kullanıcının aradığı ürünün veya isteğin olabileceği en mantıklı kategorileri
    semantik arama ile bulur.

    Args:
        sample_query: Kullanıcının niyetini anlatan cümle
                      (Örn: 'kamp için su geçirmez çadır' veya 'kırmızı elbise').

    Returns:
        JSON string formatında eşleşen kategorilerin ID, isim ve full_path bilgileri.
    """
    try:
        results = _client.search_categories(sample_query, limit=5)
        return json.dumps(results, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def get_category_filters(category_id: str) -> str:
    """
    Belirli bir kategorideki ürünleri daraltmak için hangi filtrelerin
    (örn: beden, renk, marka, fiyat) kullanılabileceğini döner.

    Args:
        category_id: Filtreleri öğrenilecek kategorinin ID'si.

    Returns:
        JSON string formatında kullanılabilir filtre listesi.
    """
    try:
        filters = _client.get_category_filters(category_id)
        return json.dumps(filters, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})
