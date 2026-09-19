"""
CatalogAPIClient — AI servisinin catalog-api ile konuştuğu HTTP istemcisi.

AI servisi bu istemci üzerinden:
  1. Kategori adaylarını sorgular   (POST /categories/vector-search)
  2. Ürün adaylarını sorgular       (POST /products/vector-search)
  3. Kategori filtrelerini öğrenir  (GET  /categories/{id}/filters)

Vektör hesaplama ve cross-encoder re-ranking AI servisinde yapılır;
bu istemci sadece ham DB sonuçlarını alır.
"""

import httpx
from chatbot.core.config import settings


class CatalogAPIClient:
    def __init__(self):
        self.base_url = settings.CATALOG_API_URL.rstrip("/")

    # ------------------------------------------------------------------
    # KATEGORİ İSTEKLERİ
    # ------------------------------------------------------------------

    def search_categories_by_vector(
        self, query_vector: list, limit: int = 20
    ) -> list:
        """
        Catalog API'ye vektörü gönderir, ham kategori adaylarını alır.
        Her eleman: { id, name, full_path, description, cosine_sim }
        """
        response = httpx.post(
            f"{self.base_url}/categories/vector-search",
            json={"query_vector": query_vector, "limit": limit},
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json().get("data", [])

    def get_category_filters(self, category_id: str) -> dict:
        """Kategoriye özel kullanılabilir filtre listesini döner."""
        response = httpx.get(
            f"{self.base_url}/categories/{category_id}/filters",
            timeout=10.0,
        )
        response.raise_for_status()
        return response.json().get("data", {})

    # ------------------------------------------------------------------
    # ÜRÜN İSTEKLERİ
    # ------------------------------------------------------------------

    def search_products_by_vector(
        self,
        query_vector: list,
        category_ids: list = None,
        brand: str = None,
        color: str = None,
        limit: int = 200,
    ) -> list:
        """
        Catalog API'ye vektör + filtreleri gönderir, ham ürün adaylarını alır.
        Her eleman: { product_id, title, description, image_url, brand, color, ... }
        Cross-encoder re-ranking bu metod dönüşünden sonra yapılır.
        """
        payload = {
            "query_vector": query_vector,
            "category_ids": category_ids or [],
            "limit": limit,
        }
        if brand:
            payload["brand"] = brand
        if color:
            payload["color"] = color

        response = httpx.post(
            f"{self.base_url}/products/vector-search",
            json=payload,
            timeout=60.0,
        )
        response.raise_for_status()
        return response.json().get("data", [])
