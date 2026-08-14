from app.infrastructure.db.db_client import DatabaseClient
from app.infrastructure.llm.ollama_client import OllamaClient
from app.services.tokenizer_service import QueryTokenizerService
from app.services.category_matcher_service import CategoryMatcherService
from app.services.product_search_service import ProductSearchService

class AppStateContainer:
    def __init__(self):
        self.ollama_client: OllamaClient = None
        self.db_client: DatabaseClient = None
        self.tokenizer_service: QueryTokenizerService = None
        self.category_matcher: CategoryMatcherService = None
        self.product_search: ProductSearchService = None

    def initialize(self):
        print("🚀 [FastAPI] Modeller ve Veritabanı bağlantıları başlatılıyor...")
        self.ollama_client = OllamaClient()
        self.db_client = DatabaseClient()
        self.tokenizer_service = QueryTokenizerService(ollama_client=self.ollama_client)
        self.category_matcher = CategoryMatcherService(db_client=self.db_client)
        
        # Share models to save RAM/VRAM
        self.product_search = ProductSearchService(
            db_client=self.db_client,
            embedding_model=self.category_matcher.embedding_model,
            cross_encoder=self.category_matcher.cross_encoder
        )
        print("✅ [FastAPI] Tüm servisler kullanıma hazır.")

    def close(self):
        print("🛑 [FastAPI] Sistem kapatılıyor...")
        if self.db_client and hasattr(self.db_client, 'conn') and self.db_client.conn:
            self.db_client.conn.close()

container = AppStateContainer()

def get_container() -> AppStateContainer:
    return container
