"""
product_service.py — Ürün semantik arama servisi.

Sorumluluk:
  1. SentenceTransformer ile query'i vektörleştir
  2. Alt kategori ID'lerini genişlet
  3. SQL filtrelerini üret (brand, color, category)
  4. pgvector + SQL filtresiyle aday ürünleri getir
  5. CrossEncoder ile re-rank yap
  6. Top-N ürünü döndür
"""

import math
from typing import Optional
from infrastructure.db_client import DatabaseClient
from infrastructure.ml_models import MLModels
from services.sql_filter_parser import SQLFilterParser


class ProductService:
    """
    Ürün arama için tam AI pipeline.
    Stateless — her istek için yeni instance yaratılır (bkz. dependencies.py).
    """

    def __init__(self, db: DatabaseClient, ml: MLModels):
        self.db = db
        self.ml = ml
        self.sql_parser = SQLFilterParser()

    # ------------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------------

    def search(
        self,
        query: str,
        category_ids: list[str] = None,
        brand: Optional[str] = None,
        color: Optional[str] = None,
        max_results: int = 10,
    ) -> list[dict]:
        """
        Doğal dil query'ini ve filtreleri alır, en alakalı ürünleri döndürür.

        Args:
            query:        Anlamsal arama sorgusu (Örn: 'su geçirmez kışlık çadır').
            category_ids: Arama yapılacak kategori ID listesi.
            brand:        Marka filtresi (opsiyonel).
            color:        Renk filtresi (opsiyonel).
            max_results:  Döndürülecek maksimum ürün sayısı.

        Returns:
            [{ product_id, title, image_url, brand, color, category_id, match_score }, ...]
        """
        if not query:
            return []

        # 1. Encode
        query_vector = self.ml.embedding_model.encode(
            query, convert_to_tensor=False
        ).tolist()

        # 2. Kategori ID genişletme
        expanded_ids = []
        if category_ids:
            expanded_ids = self.db.get_all_subcategory_ids(category_ids)
            print(
                f"    🌲 Kategori genişletme: {len(category_ids)} → {len(expanded_ids)} alt kategori"
            )

        # 3. SQL filtresi oluştur
        extracted_filters: dict = {}
        if expanded_ids:
            extracted_filters["category_taxonomy"] = expanded_ids
        if brand:
            extracted_filters["brand"] = brand
        if color:
            extracted_filters["color"] = [color]

        where_clause, filter_params = self.sql_parser.parse_filters(extracted_filters)
        print(f"    🔍 SQL WHERE: {where_clause}")

        # 4. DB'den ham adayları getir (fazladan çek, cross-encoder sıralar)
        fetch_limit = max(200, max_results * 20)
        candidates = self.db.get_products_by_vector_and_filters(
            query_vector=query_vector,
            where_clause=where_clause,
            filter_params=filter_params,
            limit=fetch_limit,
        )

        if not candidates:
            print("    ❌ Ürün adayı bulunamadı.")
            return []

        print(f"    ✅ {len(candidates)} aday bulundu. Cross-encoder sıralıyor...")

        # 5. Cross-encoder re-ranking
        cross_inp = [
            [query, f"{p.get('title', '')}. {p.get('description', '')}".strip()]
            for p in candidates
        ]
        logits = self.ml.cross_encoder.predict(cross_inp)

        for j, prod in enumerate(candidates):
            prod["cross_encoder_score"] = (
                1 / (1 + math.exp(-float(logits[j])))
            ) * 100

        candidates.sort(key=lambda x: x["cross_encoder_score"], reverse=True)

        top = candidates[:max_results]
        self._log_results(top)

        return [
            {
                "product_id": str(p.get("product_id", "")),
                "title": p.get("title", ""),
                "image_url": p.get("image_url"),
                "brand": p.get("brand"),
                "color": p.get("color"),
                "category_id": str(p.get("category_id", "")),
                "match_score": f"{p.get('cross_encoder_score', 0):.1f}%",
            }
            for p in top
        ]

    # ------------------------------------------------------------------
    # PRIVATE HELPERS
    # ------------------------------------------------------------------

    def _log_results(self, results: list[dict]) -> None:
        print(f"\n🏆 [ProductService] İlk {min(5, len(results))} Ürün:")
        for idx, p in enumerate(results[:5], 1):
            print(
                f"  {idx}. [{p.get('match_score', '?')}] "
                f"{p.get('title', '?')} (Kategori: {p.get('category_id', '?')})"
            )
