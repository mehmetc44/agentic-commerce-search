import json
from app.infrastructure.db.db_client import DatabaseClient
from app.infrastructure.llm.ollama_client import OllamaClient
from app.services.tokenizer_service import QueryTokenizerService
from app.services.category_matcher_service import CategoryMatcherService
from app.services.product_search_service import ProductSearchService

def run_hybrid_search_pipeline(user_query: str):
    # Dependency Injection & Initialization
    ollama_client = OllamaClient()
    db_client = DatabaseClient()
    
    tokenizer_service = QueryTokenizerService(ollama_client=ollama_client)
    category_matcher = CategoryMatcherService(db_client=db_client)
    
    # Reuse models to save VRAM/RAM
    product_search = ProductSearchService(
        db_client=db_client,
        embedding_model=category_matcher.embedding_model,
        cross_encoder=category_matcher.cross_encoder
    )

    print(f"🔍 [STAGE 1] Kullanıcı Sorgusu Anlamlandırılıyor: '{user_query}'")
    # Stage 1: JSON generation and query sanitization
    stage1_json = tokenizer_service.tokenize_user_query(user_query)
    
    # Retrieve the rich vector query string
    rewritten_query = stage1_json["analysis"]["rewritten_query"]
    print(f"   -> Üretilen Vektör Sorgusu: '{rewritten_query}'\n")

    print(f"🌲 [STAGE 2] Kategori Eşleştirme Motoru Çalıştırılıyor...")
    # Stage 2: Retrieve matching category IDs
    matched_ids = category_matcher.get_matched_category_ids(rewritten_query)
    print(f"   -> Eşleşme Sınırını Geçen Kategori ID'leri: {matched_ids}\n")

    # Inject the matched category IDs into taxonomy filter
    stage1_json["analysis"]["extracted_filters"]["category_taxonomy"] = matched_ids

    print("🎉 [STAGE 1 & 2 TAMAMLANDI] Ara Çıktı JSON:")
    print(json.dumps(stage1_json, indent=2, ensure_ascii=False))
    
    print(f"\n🚀 [STAGE 3] Ürün Filtreleme ve Vektör Araması Başlıyor...")
    # Stage 3: Retrieve products with SQL filters + vector search, and rerank
    top_products = product_search.search_products(final_json=stage1_json, max_results=50)
    
    print(f"\n✅ Pipeline başarıyla tamamlandı. Önerilen toplam ürün sayısı: {len(top_products)}")
    return top_products
