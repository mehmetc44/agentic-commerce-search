from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    # Zorunlu alanları opsiyonel veya varsayılanlı yapıyoruz
    parent_asin: str = ""
    title: str = ""
    description: str = ""
    main_category: str = ""
    categories: str = ""
    store: str = ""
    
    # Sayısal Alanlar
    average_rating: float = 0.0
    rating_number: int = 0
    price: float = 0.0
    index_level_0: int = 0
    
    # Detay ve Görsel Alanları
    features: str = ""
    details: str = ""
    image: str = ""
    
    # Arama Sorguları (LLM tarafından üretilen)
    query_1: str = ""
    query_2: str = ""
    query_3: str = ""

    def __str__(self):
        return f"<Product: {self.title[:30]}... | Price: {self.price} | Category: {self.main_category}>"