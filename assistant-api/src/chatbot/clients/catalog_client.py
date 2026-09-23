"""
catalog_client.py — AI servisinin catalog-api ile konuştuğu HTTP istemcisi.

catalog-api artık tüm AI işlemlerini (embedding, cross-encoder) kendi içinde yapıyor.
Bu istemci sadece doğal dil metni gönderir, hazır sıralanmış sonuçları alır.
"""

import httpx
from chatbot.core.config import settings


class CatalogAPIClient:
    def __init__(self):
        self.base_url = settings.CATALOG_API_URL.rstrip("/")

    # ------------------------------------------------------------------
    # KATEGORİ
    # ------------------------------------------------------------------

    def get_closest_categories(self, vector: list[float], limit: int = 5) -> list:
        """
        Vektör gönderir, cosine similarity'ye göre sıralanmış kategori listesi alır.

        Returns:
            [{ id, name, full_path, similarity }, ...]
        """
        response = httpx.post(
            f"{self.base_url}/categories/closest",
            json={"vector": vector, "limit": limit},
            timeout=10.0,
        )
        response.raise_for_status()
        return response.json()

    def get_category_filters(self, category_id: str) -> dict:
        """Kategoriye özel kullanılabilir filtre listesini döner."""
        response = httpx.get(
            f"{self.base_url}/categories/{category_id}/filters",
            timeout=10.0,
        )
        response.raise_for_status()
        return response.json().get("data", {})

    # ------------------------------------------------------------------
    # ÜRÜN
    # ------------------------------------------------------------------

    def search_products(
        self,
        query: str,
        category_ids: list = None,
        brand: str = None,
        color: str = None,
        max_results: int = 10,
    ) -> list:
        """
        Doğal dil query'i ve filtreleri gönderir, sıralanmış ürün listesi alır.
        Embedding ve cross-encoder catalog-api tarafında çalışır.

        Returns:
            [{ product_id, title, image_url, brand, color, category_id, match_score }, ...]
        """
        payload = {
            "query": query,
            "category_ids": category_ids or [],
            "max_results": max_results,
        }
        if brand:
            payload["brand"] = brand
        if color:
            payload["color"] = color

        response = httpx.post(
            f"{self.base_url}/products/search",
            json=payload,
            timeout=120.0,
        )
        response.raise_for_status()
        return response.json().get("data", [])
