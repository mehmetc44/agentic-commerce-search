from pydantic import BaseModel
from typing import Union


class CategorySearchRequest(BaseModel):
    """POST /categories/search için istek modeli."""
    query: str
    limit: int = 5


class CategoryResult(BaseModel):
    """Tek bir kategori sonucu."""
    id: Union[str, int]
    name: str
    full_path: str
    confidence: float


class CategoryListResponse(BaseModel):
    """GET /categories için yanıt."""
    data: list[dict]


class CategorySearchResponse(BaseModel):
    """POST /categories/search için yanıt."""
    data: list[CategoryResult]


class CategoryFiltersResponse(BaseModel):
    """GET /categories/{id}/filters için yanıt."""
    data: dict
