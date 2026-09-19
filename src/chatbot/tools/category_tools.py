"""
category_tools.py — LangGraph için kategori arama tool'ları

Akış:
  1. Query'i embedding_model ile vektörleştir
  2. Vektörü catalog-api'ye gönder  →  ham kategori adayları al
  3. Cross-encoder ile re-rank yap
  4. Eşiği geçen top-5 kategoriyi LLM'e dön
"""

from langchain_core.tools import tool
import json
import math
from chatbot.services.container import container


def _clean_query(raw_query: str) -> str:
    """
    Tekrarlı token'ları ve fiyat ifadelerini temizler.
    Embedding kalitesini artırmak için gürültüyü azaltır.
    """
    if not raw_query:
        return ""
    tokens = [t.strip() for t in raw_query.split(",")]
    unique_tokens = list(dict.fromkeys(tokens))
    final_tokens = [t for t in unique_tokens if not any(ch.isdigit() for ch in t)]
    return " ".join(final_tokens)


@tool
def get_closest_categories(sample_query: str) -> str:
    """
    Kullanıcının aradığı ürünün veya isteğin olabileceği en mantıklı kategorileri
    semantik (vektör + cross-encoder) arama ile bulur.

    Args:
        sample_query: Kullanıcının niyetini anlatan cümle
                      (Örn: 'kamp için su geçirmez çadır' veya 'kırmızı elbise').

    Returns:
        JSON string formatında eşleşen kategorilerin ID, isim ve full_path bilgileri.
    """
    try:
        # 1. Sorguyu temizle ve vektörleştir
        clean_query = _clean_query(sample_query)
        query_vector = container.embedding_model.encode(
            clean_query, convert_to_tensor=False
        ).tolist()

        # 2. catalog-api'den ham kategori adaylarını al (pgvector araması)
        candidates = container.catalog_client.search_categories_by_vector(
            query_vector=query_vector, limit=20
        )

        if not candidates:
            return json.dumps([], ensure_ascii=False)

        # 3. Cross-encoder ile re-ranking
        cross_inp = [
            [clean_query, c.get("description", "") or ""] for c in candidates
        ]
        cross_logits = container.cross_encoder.predict(cross_inp)

        threshold = 20.0  # %20 güven eşiği
        scored = []
        for j, cat in enumerate(candidates):
            score_pct = (1 / (1 + math.exp(-float(cross_logits[j])))) * 100
            cat["confidence"] = score_pct
            scored.append(cat)

        scored.sort(key=lambda x: x["confidence"], reverse=True)

        # Eşiği geçenleri al; geçen yoksa top-5'i dön
        passed = [c for c in scored if c["confidence"] >= threshold]
        top_results = passed[:5] if passed else scored[:5]

        print(f"⚙️ Kategori Cross-Encoder (threshold: %{threshold:.0f})")
        for idx, c in enumerate(top_results, 1):
            print(f"  {idx}. %{c['confidence']:.1f}  |  {c['full_path']}")

        results = [
            {"id": c["id"], "name": c["name"], "full_path": c["full_path"]}
            for c in top_results
        ]
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
        filters = container.catalog_client.get_category_filters(category_id)
        return json.dumps(filters, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})
