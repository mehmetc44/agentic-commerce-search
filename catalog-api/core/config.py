import os
from dotenv import load_dotenv

load_dotenv()


class CatalogSettings:
    """
    Catalog API için ayarlar. Sadece veritabanı bağlantısı.
    Yapay zeka modeli veya LLM ayarı içermez.
    """

    DB_PARAMS: dict = {
        "dbname": os.getenv("DB_NAME", "e-commerce"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "admin123"),
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", 5432)),
    }


settings = CatalogSettings()
