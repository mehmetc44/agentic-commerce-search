"""
ml_models.py — SentenceTransformer ve CrossEncoder singleton yükleyicisi.

catalog-api başladığında (FastAPI lifespan) 1 kez yüklenir.
Tüm servisler dependency injection ile bu instance'ı alır.
"""

import torch
from sentence_transformers import SentenceTransformer, CrossEncoder
from core.config import settings


class MLModels:
    """
    Embedding ve re-ranking modellerini barındıran container.
    Doğrudan örnekleme yerine dependencies.py üzerinden kullanılır.
    """

    def __init__(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"⏳ [MLModels] Cihaz: {device.upper()}")

        print(f"⏳ [MLModels] SentenceTransformer yükleniyor: {settings.EMBEDDING_MODEL_PATH}")
        self.embedding_model = SentenceTransformer(
            settings.EMBEDDING_MODEL_PATH, device=device
        )

        print(f"⏳ [MLModels] CrossEncoder yükleniyor: {settings.CROSS_ENCODER_PATH}")
        self.cross_encoder = CrossEncoder(
            settings.CROSS_ENCODER_PATH, device=device
        )

        print("✅ [MLModels] Tüm modeller yüklendi.")
