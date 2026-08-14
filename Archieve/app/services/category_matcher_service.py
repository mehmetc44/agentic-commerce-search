import math
import torch
from sentence_transformers import SentenceTransformer, CrossEncoder
from app.core.config import settings
from app.infrastructure.db.db_client import DatabaseClient

class CategoryMatcherService:
    """
    Stage 2: Two-Stage Semantic Search (Bi-Encoder Retrieval + Cross-Encoder Rerank)
    """
    def __init__(self, db_client: DatabaseClient):
        self.db_client = db_client
        print("⏳ [CategoryMatcher] Modeller RAM'e yükleniyor...")
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL_PATH, device=self.device)
        self.cross_encoder = CrossEncoder(settings.CROSS_ENCODER_PATH, device=self.device)
        self.threshold_pct = settings.CATEGORY_CONFIDENCE_THRESHOLD

    def _clean_query_for_semantic_models(self, raw_query: str) -> str:
        """Ollama'dan gelen tekrarlı ve fiyat içeren gürültülü vektör metnini yapay zeka için temizler."""
        if not raw_query:
            return ""
            
        # 1. Virgüllerden ayır ve boşlukları temizle
        tokens = [t.strip() for t in raw_query.split(',')]
        
        # 2. Tekrar eden kelimeleri sırayı bozmadan teke düşür
        unique_tokens = list(dict.fromkeys(tokens))
        
        # 3. İçinde rakam olan (örn: 1000, 50) fiyat belirteçlerini sil
        final_tokens = [t for t in unique_tokens if not any(char.isdigit() for char in t)]
        return " ".join(final_tokens)

    def get_matched_category_ids(self, rewritten_query: str) -> list:
        if not rewritten_query:
            return []
        clean_query = self._clean_query_for_semantic_models(rewritten_query)
        print(f"    🧹 Yapay Zeka İçin Temizlenen Sorgu: '{clean_query}'")

        # ==========================================
        # AŞAMA 1: BI-ENCODER RETRIEVAL 
        # ==========================================
        query_vector = self.embedding_model.encode(clean_query, convert_to_tensor=False).tolist()
        candidates = self.db_client.get_top_candidates_by_vector(query_vector, limit=20)
        
        if not candidates:
            return []

        # ==========================================
        # AŞAMA 2: CROSS-ENCODER RERANKING
        # ==========================================
        cross_inp = [[clean_query, cat["description"]] for cat in candidates]
        cross_logits = self.cross_encoder.predict(cross_inp)
        
        # Skorları hesapla ve dictionary'e yaz
        for j, cat in enumerate(candidates):
            score_pct = (1 / (1 + math.exp(-float(cross_logits[j])))) * 100
            cat["confidence"] = score_pct
            
        # Skorlara göre büyükten küçüğe sırala
        candidates.sort(key=lambda x: x["confidence"], reverse=True)
        
        passed_categories = [c for c in candidates if c["confidence"] >= self.threshold_pct]
        
        # ==========================================
        # ŞEFFAF LOGLAMA (Sorunu Görmek İçin)
        # ==========================================
        print(f"\n⚙️ Cross-Encoder Sonuçları (Threshold: %{self.threshold_pct:.1f})")

        if passed_categories:
            print(f"✅ Eşiği geçen kategori sayısı: {len(passed_categories)}\n")
            for idx, cat in enumerate(passed_categories, start=1):
                print(
                    f"{idx:2d}. %{cat['confidence']:.2f}  |  {cat['full_path']}")
        else:
            print("❌ Hiçbir kategori threshold'u geçemedi.\n")
            print("📊 En yüksek skorlu 3 aday:")
            for idx, cat in enumerate(candidates[:3], start=1):
                print(f"{idx:2d}. %{cat['confidence']:.2f}  |  {cat['full_path']}")

        print("-" * 80)

        return [c["id"] for c in passed_categories]
