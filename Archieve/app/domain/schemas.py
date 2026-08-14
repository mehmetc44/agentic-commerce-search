from pydantic import BaseModel, Field
from typing import List, Optional

class SearchRequest(BaseModel):
    query: str = Field(..., description="The user's natural language search query", example="I'm looking for affordable waterproof winter boots for my baby girl, preferably in black or brown, with a budget of no more than 1000 TL")

class ProductResponse(BaseModel):
    product_id: str
    title: str
    description: Optional[str]
    category_taxonomy: Optional[str]
    image_url: Optional[str]
    brand: Optional[str]
    color: Optional[str]
    material: Optional[str]
    style: Optional[str]
    product_type: Optional[str]
    model_year: Optional[str]
    clean_path: Optional[str]
    category_id: Optional[str]
    cosine_sim: float
    cross_encoder_score: float

class SearchResponse(BaseModel):
    original_query: str
    rewritten_query: str
    extracted_filters: dict
    total_found: int
    products: List[ProductResponse]
