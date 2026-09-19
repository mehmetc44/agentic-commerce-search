import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    AI servisi (chatbot) için ayarlar.
    Sadece LLM ve catalog-api bağlantısı içerir.
    ML model path'leri catalog-api'ye taşındı.
    """

    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "deepseek")

    # DeepSeek API
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

    # Ollama (Opsiyonel)
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen3.5:4b")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    # Catalog API — tüm DB ve AI arama işlemleri bu serviste
    CATALOG_API_URL: str = os.getenv("CATALOG_API_URL", "http://localhost:8001")


settings = Settings()
