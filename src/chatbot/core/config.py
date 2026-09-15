import os
from dotenv import load_dotenv

# Load env variables from .env file
load_dotenv()

class Settings:
    """
    Project settings loaded from environment variables.
    """
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "deepseek")
    
    # DeepSeek API Settings
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    
    # Ollama Settings (Optional)
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen3.5:4b")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # Veritabanı Ayarları
    DB_PARAMS: dict = {
        "dbname": os.getenv("DB_NAME", "e-commerce"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "admin123"),
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", 5432))
    }

    # Fine-Tuned Model Yolları
    EMBEDDING_MODEL_PATH: str = os.getenv("EMBEDDING_MODEL_PATH", "sentence-transformers/all-MiniLM-L6-v2")
    CROSS_ENCODER_PATH: str = os.getenv("CROSS_ENCODER_PATH", "cross-encoder/ms-marco-MiniLM-L-6-v2")
    
    # Kategori Eşleşme Güven Eşiği (%85)
    CATEGORY_CONFIDENCE_THRESHOLD: float = float(os.getenv("CATEGORY_CONFIDENCE_THRESHOLD", 20.0))

settings = Settings()
