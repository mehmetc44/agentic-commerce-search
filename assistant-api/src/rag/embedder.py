import os
from langchain_huggingface import HuggingFaceEmbeddings
from core.config import settings, agent_config

class CatalogEmbedder:
    """
    Agentic Commerce için lokal vektör oluşturma (Embedding) servisi.
    Modeli belirtilen path'ten veya HuggingFace'ten indirip kullanır.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CatalogEmbedder, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
        
    def _initialize(self):
        # Config'den cache yolunu oku
        cache_dir = settings.EMBEDDING_MODEL_PATH
        
        # Model ismini ve parametreleri yaml'dan oku
        embed_config = agent_config.get("embedding", {})
        model_name = embed_config.get("model", "Trendyol/TY-ecomm-embed-multilingual-base-v1.2.0")
        device = embed_config.get("device", "cpu")
            
        print(f"Embedding Modeli Yükleniyor: {model_name} (Lokal Path: {cache_dir}, Device: {device})...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            cache_folder=cache_dir,
            model_kwargs={
                'trust_remote_code': True,
                'device': device
            }
        )

    def embed_query(self, query: str) -> list[float]:
        """Tek bir kelime/cümle için vektör oluşturur."""
        return self.embeddings.embed_query(query)
        
    def embed_documents(self, documents: list[str]) -> list[list[float]]:
        """Birden fazla kelime/cümle için vektörler oluşturur."""
        return self.embeddings.embed_documents(documents)

# Her import edildiğinde tekrar belleğe yüklememek için Singleton instance
embedder = CatalogEmbedder()
