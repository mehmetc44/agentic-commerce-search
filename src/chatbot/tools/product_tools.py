"""
product_tools.py — LangGraph için ürün arama tool'u

Akış:
  1. product_query'i embedding_model ile vektörleştir
  2. Vektör + filtreleri catalog-api'ye gönder  →  ham ürün adayları al
  3. Cross-encoder ile re-rank yap
  4. Top-10 ürünü LLM'e dön
"""

from langchain_core.tools import tool
import json
import math
from typing import List, Optional
from chatbot.services.container import container


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
    Verilen kategori ID'lerinde ve filtrelerde ürün arar.
    Vektör benzerliği ile aday ürünleri bulur, cross-encoder ile sıralar.

    Args:
        category_ids:  Ürünlerin aranacağı kategori ID'leri (Örn: ["101", "102"]).
        product_query: Anlamsal arama için sorgu cümlesi
                       (Örn: 'su geçirmez kışlık çadır').
        brand:         (Opsiyonel) Marka filtresi.
        color:         (Opsiyonel) Renk filtresi.
        min_price:     (Opsiyonel) Minimum fiyat.
        max_price:     (Opsiyonel) Maksimum fiyat.

    Returns:
        JSON string formatında önerilen ürünler listesi.
    """
    try:
        # 1. Sorguyu vektörleştir
        query_vector = container.embedding_model.encode(
            product_query, convert_to_tensor=False
        ).tolist()

        # 2. catalog-api'den ham ürün adaylarını al
        candidates = container.catalog_client.search_products_by_vector(
            query_vector=query_vector,
            category_ids=category_ids,
            brand=brand,
            color=color,
            limit=200,
        )

        if not candidates:
            print("    ❌ Ürün adayı bulunamadı.")
            return json.dumps([], ensure_ascii=False)

        print(f"    ✅ {len(candidates)} ham aday alındı. Cross-encoder ile sıralanıyor...")

        # 3. Cross-encoder ile re-ranking
        cross_inp = []
        for prod in candidates:
            title = str(prod.get("title") or "")
            desc = str(prod.get("description") or "")
            cross_inp.append([product_query, f"{title}. {desc}".strip()])

        cross_logits = container.cross_encoder.predict(cross_inp)

        for j, prod in enumerate(candidates):
            score_pct = (1 / (1 + math.exp(-float(cross_logits[j])))) * 100
            prod["cross_encoder_score"] = score_pct

        candidates.sort(key=lambda x: x["cross_encoder_score"], reverse=True)

        # 4. Top-10 ürünü döndür
        top_products = candidates[:10]

        print("\n🏆 İlk 5 Önerilen Ürün:")
        for idx, p in enumerate(top_products[:5], 1):
            print(
                f"  {idx}. [%{p['cross_encoder_score']:.1f}] "
                f"{p['title']} (Kategori ID: {p['category_id']})"
            )

        results = [
            {
                "product_id": p.get("product_id"),
                "title": p.get("title"),
                "price": 0,
                "category_id": p.get("category_id"),
                "image_url": p.get("image_url"),
                "brand": p.get("brand"),
                "color": p.get("color"),
                "match_score": f"{p.get('cross_encoder_score', 0):.1f}%",
            }
            for p in top_products
        ]
        return json.dumps(results, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"error": str(e)})
