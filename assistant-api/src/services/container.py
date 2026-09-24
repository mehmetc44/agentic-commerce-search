"""
container.py — AI servisi için singleton kaynak yöneticisi.

Chatbot artık hiçbir ML modeli yüklemez.
Tüm AI işlemleri (embedding, cross-encoder) catalog-api'de yapılır.

Bu container sadece CatalogAPIClient'ı başlatır.
"""

from clients.catalog_client import CatalogAPIClient
from core.config import settings


class ServicesContainer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ServicesContainer, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        print(f"⏳ [Chatbot] Catalog API bağlantısı kuruluyor: {settings.CATALOG_API_URL}")
        self.catalog_client = CatalogAPIClient()
        print("✅ [Chatbot] Hazır. (AI modelleri catalog-api'de çalışıyor)")


# Global singleton
container = ServicesContainer()
