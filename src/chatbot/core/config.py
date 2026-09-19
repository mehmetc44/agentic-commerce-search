import os
from dotenv import load_dotenv

# Load env variables from .env file
load_dotenv()


class Settings:
    """
    AI servisi için ayarlar. Sadece LLM ve AI model konfigürasyonu içerir.
    Veritabanı bağlantısı catalog-api servisinde yönetilir.
    """

    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "deepseek")

    # DeepSeek API Settings
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

    # Ollama Settings (Opsiyonel)
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen3.5:4b")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    # Fine-Tuned Model Yolları (AI servisi içinde çalışır)
    EMBEDDING_MODEL_PATH: str = os.getenv(
        "EMBEDDING_MODEL_PATH", "sentence-transformers/all-MiniLM-L6-v2"
    )
    CROSS_ENCODER_PATH: str = os.getenv(
        "CROSS_ENCODER_PATH", "cross-encoder/ms-marco-MiniLM-L-6-v2"
    )

    # Kategori Eşleşme Güven Eşiği
    CATEGORY_CONFIDENCE_THRESHOLD: float = float(
        os.getenv("CATEGORY_CONFIDENCE_THRESHOLD", 20.0)
    )

    # Catalog API URL — DB ve ürün/kategori işlemleri bu serviste yapılır
    CATALOG_API_URL: str = os.getenv("CATALOG_API_URL", "http://localhost:8001")


settings = Settings()
