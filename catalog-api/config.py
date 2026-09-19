import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_NAME: str = os.getenv("DB_NAME", "e-commerce")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "admin123")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))
    
    EMBEDDING_MODEL_PATH: str = os.getenv("EMBEDDING_MODEL_PATH", "../shared/ai-models/embeddings")

settings = Settings()
