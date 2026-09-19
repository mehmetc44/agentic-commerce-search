"""
ServicesContainer — AI servisi için singleton kaynak yöneticisi.

Başlatılan kaynaklar:
  - SentenceTransformer  (embedding modeli — sorguları vektörleştirir)
  - CrossEncoder         (re-ranking modeli — adayları sıralar)
  - CatalogAPIClient     (catalog-api HTTP istemcisi — ham DB sonuçlarını getirir)

Veritabanı bağlantısı, kategori eşleme ve ürün arama servisleri
artık catalog-api'de yaşar. Bu container sadece AI model kaynaklarını tutar.
"""

import torch
from sentence_transformers import SentenceTransformer, CrossEncoder
from chatbot.core.config import settings
from chatbot.clients.catalog_client import CatalogAPIClient


class ServicesContainer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ServicesContainer, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        print("⏳ [AI Container] AI modelleri yükleniyor (Bu işlem 1 kez yapılır)...")

        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"    📟 Cihaz: {device.upper()}")

        print("⏳ [AI Container] SentenceTransformer yükleniyor...")
        self.embedding_model = SentenceTransformer(
            settings.EMBEDDING_MODEL_PATH, device=device
        )

        print("⏳ [AI Container] CrossEncoder yükleniyor...")
        self.cross_encoder = CrossEncoder(
            settings.CROSS_ENCODER_PATH, device=device
        )

        print("⏳ [AI Container] Catalog API istemcisi başlatılıyor...")
        self.catalog_client = CatalogAPIClient()

        print(f"✅ [AI Container] Hazır. Catalog API: {settings.CATALOG_API_URL}")


# Global singleton
container = ServicesContainer()
