"""
Embedding Service
Sorumluluğu: Metinlerden pgvector'e uygun vector (float listesi) üretmek.
Model: all-MiniLM-L6-v2 (384 boyut)
"""
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
        
    def _initialize(self):
        # Model is loaded once (Singleton)
        logger.info("Loading embedding model (all-MiniLM-L6-v2)...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        logger.info("Embedding model loaded successfully.")

    def embed(self, text: str) -> list[float]:
        """
        Metinden vector üretir.
        """
        # encode returns a numpy array, we convert it to python list of floats
        vector = self.model.encode(text)
        return vector.tolist()

# Global instance
embedding_service = EmbeddingService()
