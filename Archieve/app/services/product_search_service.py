import math
import torch
from sentence_transformers import SentenceTransformer, CrossEncoder
from app.core.config import settings
from app.infrastructure.db.db_client import DatabaseClient
from app.services.sql_filter_parser import SQLFilterParser

class ProductSearchService:
    """
    Stage 3: Son JSON'u alıp, Regex Parser ile filtreleyen, 
    vektör araması yapan ve Cross-Encoder ile re-ranking uygulayan servis.
    """
    def __init__(self, db_client: DatabaseClient, embedding_model=None, cross_encoder=None):
        self.db_client = db_client
        self.sql_parser = SQLFilterParser()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # RAM tasarrufu için önceki servisteki modelleri tekrar kullanabiliriz
        if embedding_model:
            self.embedding_model = embedding_model
        else:
            print("⏳ [ProductSearch] Embedding Model yükleniyor...")
            self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL_PATH, device=self.device)
            
        if cross_encoder:
            self.cross_encoder = cross_encoder
        else:
            print("⏳ [ProductSearch] Cross-Encoder yükleniyor...")
            self.cross_encoder = CrossEncoder(settings.CROSS_ENCODER_PATH, device=self.device)

    def search_products(self, final_json: dict, max_results: int = 50) -> list:
        # 1. Kategori ID'lerini alt kategorileri içerecek şekilde genişlet
        extracted_filters = final_json.get("analysis", {}).get("extracted_filters", {})
        category_taxonomy = extracted_filters.get("category_taxonomy", [])
        if category_taxonomy:
            expanded_ids = self.db_client.get_all_subcategory_ids(category_taxonomy)
            print(f"    🌲 Kategori Genişletme: {len(category_taxonomy)} kategori -> {len(expanded_ids)} alt kategoriye genişletildi.")
            extracted_filters["category_taxonomy"] = expanded_ids

        # 2. Regex Parser ile filtreleri SQL'e dönüştür
        where_clause, filter_params = self.sql_parser.parse_filters(extracted_filters)
        print(f"    🔍 Üretilen SQL WHERE: {where_clause}")
        print(f"    🔍 Parametreler: {filter_params}")
        
        # 2. rewritten_query embedding'ini çıkar
        rewritten_query = final_json.get("analysis", {}).get("rewritten_query", "")
        if not rewritten_query:
            print("⚠️ Boş sorgu, arama yapılamıyor.")
            return []
            
        print(f"    🧠 Vektörleştirilen Sorgu: '{rewritten_query}'")
        query_vector = self.embedding_model.encode(rewritten_query, convert_to_tensor=False).tolist()
        
        # 3. Veritabanından SQL Filtresi + Cosine Similarity (pgvector) ile candidate ürünleri çek
        db_fetch_limit = max(200, max_results * 4) 
        print(f"    📥 Veritabanından aday ürünler çekiliyor (Limit: {db_fetch_limit})...")
        candidates = self.db_client.get_products_by_vector_and_filters(
            query_vector=query_vector, 
            where_clause=where_clause, 
            filter_params=filter_params, 
            limit=db_fetch_limit
        )
        
        if not candidates:
            print("    ❌ Filtrelere ve vektör aramasına uygun ürün bulunamadı.")
            return []
            
        print(f"    ✅ {len(candidates)} adet aday ürün bulundu. Cross-Encoder ile sıralanıyor...")
        
        # 4. Cross-Encoder ile Re-ranking
        cross_inp = []
        for prod in candidates:
            title = str(prod.get("title") or "")
            desc = str(prod.get("description") or "")
            product_text = f"{title}. {desc}".strip()
            cross_inp.append([rewritten_query, product_text])
            
        cross_logits = self.cross_encoder.predict(cross_inp)
        
        for j, prod in enumerate(candidates):
            # Sigmoid fonksiyonu ile skoru 0-100 arasına çek
            score_pct = (1 / (1 + math.exp(-float(cross_logits[j])))) * 100
            prod["cross_encoder_score"] = score_pct
            
        # Skorlara göre büyükten küçüğe sırala
        candidates.sort(key=lambda x: x["cross_encoder_score"], reverse=True)
        
        # 5. Top N ürün döndür
        top_products = candidates[:max_results]
        
        print(f"\n🏆 İlk 5 Önerilen Ürün:")
        for idx, p in enumerate(top_products[:5], 1):
            print(f"  {idx}. [Skor: %{p['cross_encoder_score']:.1f}] {p['title']} (Kategori ID: {p['category_id']})")
            
        return top_products
