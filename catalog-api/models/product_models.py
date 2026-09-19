from pydantic import BaseModel
from typing import Optional


class ProductSearchRequest(BaseModel):
    """POST /products/search için istek modeli."""
    query: str
    category_ids: list[str] = []
    brand: Optional[str] = None
    color: Optional[str] = None
    max_results: int = 10


class ProductResult(BaseModel):
    """Tek bir ürün sonucu."""
    product_id: str
    title: str
    image_url: Optional[str] = None
    brand: Optional[str] = None
    color: Optional[str] = None
    category_id: Optional[str] = None
    match_score: str


class ProductSearchResponse(BaseModel):
    """POST /products/search için yanıt."""
    data: list[ProductResult]


class ProductDetailResponse(BaseModel):
    """GET /products/{id} için yanıt."""
    data: dict


class ProductListResponse(BaseModel):
    """GET /products/category/{id} için yanıt."""
    data: list[dict]
