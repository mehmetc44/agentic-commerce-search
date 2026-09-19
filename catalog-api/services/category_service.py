"""
category_service.py — Kategori semantik arama servisi.

Sorumluluk:
  1. Ham query'i temizle (tekrar, rakam gürültüsü)
  2. SentenceTransformer ile vektörleştir
  3. pgvector ile top-20 aday kategori getir
  4. CrossEncoder ile re-rank yap
  5. Güven eşiğini geçen top-N kategoriyi döndür
"""

import math
from infrastructure.db_client import DatabaseClient
from infrastructure.ml_models import MLModels
from core.config import settings


class CategoryService:
    """
    Kategori arama için tam AI pipeline.
    Stateless — her istek için yeni instance yaratılır (bkz. dependencies.py).
    """

    def __init__(self, db: DatabaseClient, ml: MLModels):
        self.db = db
        self.ml = ml
        self.threshold = settings.CATEGORY_CONFIDENCE_THRESHOLD

    # ------------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------------

    def search(self, query: str, limit: int = 5) -> list[dict]:
        """
        Doğal dil query'ini alır, en alakalı kategorileri döndürür.

        Args:
            query: Kullanıcı sorgusunu anlatan metin (Örn: 'kırmızı elbise').
            limit: Döndürülecek maksimum kategori sayısı.

        Returns:
            [{ id, name, full_path, confidence }, ...]
        """
        clean = self._clean_query(query)
        if not clean:
            return []

        # 1. Encode
        query_vector = self.ml.embedding_model.encode(
            clean, convert_to_tensor=False
        ).tolist()

        # 2. pgvector — top-20 aday
        candidates = self.db.get_top_candidates_by_vector(query_vector, limit=20)
        if not candidates:
            return []

        # 3. Cross-encoder re-ranking
        cross_inp = [
            [clean, c.get("description", "") or ""] for c in candidates
        ]
        logits = self.ml.cross_encoder.predict(cross_inp)

        for j, cat in enumerate(candidates):
            cat["confidence"] = (1 / (1 + math.exp(-float(logits[j])))) * 100

        candidates.sort(key=lambda x: x["confidence"], reverse=True)

        # 4. Eşik filtresi
        passed = [c for c in candidates if c["confidence"] >= self.threshold]
        top = passed[:limit] if passed else candidates[:limit]

        self._log_results(top)

        return [
            {
                "id": c["id"],
                "name": c["name"],
                "full_path": c["full_path"],
                "confidence": round(c["confidence"], 2),
            }
            for c in top
        ]

    # ------------------------------------------------------------------
    # PRIVATE HELPERS
    # ------------------------------------------------------------------

    def _clean_query(self, raw: str) -> str:
        """
        Tekrarlı token'ları ve rakam içeren ifadeleri temizler.
        Embedding kalitesini artırmak için gürültüyü azaltır.
        """
        if not raw:
            return ""
        tokens = [t.strip() for t in raw.split(",")]
        unique = list(dict.fromkeys(tokens))
        filtered = [t for t in unique if not any(ch.isdigit() for ch in t)]
        return " ".join(filtered)

    def _log_results(self, results: list[dict]) -> None:
        print(f"\n⚙️  [CategoryService] Sonuçlar (threshold: %{self.threshold:.0f})")
        for idx, c in enumerate(results, 1):
            print(f"  {idx}. %{c['confidence']:.1f}  |  {c['full_path']}")
