import torch
from sentence_transformers import SentenceTransformer, CrossEncoder
from chatbot.core.config import settings
from chatbot.infrastructure.db_client import DatabaseClient
from chatbot.services.category_matcher_service import CategoryMatcherService
from chatbot.services.product_search_service import ProductSearchService

class ServicesContainer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ServicesContainer, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        print("⏳ [Container] Servisler ve Yapay Zeka modelleri başlatılıyor (Bu işlem 1 kez yapılır)...")
        self.db_client = DatabaseClient()
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print("⏳ [Container] SentenceTransformer Yükleniyor...")
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL_PATH, device=device)
        
        print("⏳ [Container] CrossEncoder Yükleniyor...")
        self.cross_encoder = CrossEncoder(settings.CROSS_ENCODER_PATH, device=device)
        
        self.category_matcher = CategoryMatcherService(self.db_client)
        # Category matcher creates its own models if not injected, but we modified it? Wait, let's inject.
        self.category_matcher.embedding_model = self.embedding_model
        self.category_matcher.cross_encoder = self.cross_encoder
        
        self.product_search = ProductSearchService(
            db_client=self.db_client,
            embedding_model=self.embedding_model,
            cross_encoder=self.cross_encoder
        )
        print("✅ [Container] Tüm servisler başarıyla yüklendi!")

# Global singleton
container = ServicesContainer()
