import os
from dotenv import load_dotenv

load_dotenv()


class CatalogSettings:
    """
    Catalog API için tüm ayarlar.
    Veritabanı bağlantısı ve ML model path'lerini .env'den okur.
    """

    # Veritabanı
    DB_PARAMS: dict = {
        "dbname": os.getenv("DB_NAME", "e-commerce"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "admin123"),
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", 5432)),
    }

    # ML Modelleri
    EMBEDDING_MODEL_PATH: str = os.getenv(
        "EMBEDDING_MODEL_PATH", "sentence-transformers/all-MiniLM-L6-v2"
    )
    CROSS_ENCODER_PATH: str = os.getenv(
        "CROSS_ENCODER_PATH", "cross-encoder/ms-marco-MiniLM-L-6-v2"
    )

    # Kategori güven eşiği (%20 varsayılan)
    CATEGORY_CONFIDENCE_THRESHOLD: float = float(
        os.getenv("CATEGORY_CONFIDENCE_THRESHOLD", 20.0)
    )


settings = CatalogSettings()
