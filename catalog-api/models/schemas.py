from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import date

# ----------------- CATEGORY SCHEMAS -----------------
class CategoryBase(BaseModel):
    name: str
    level: int
    full_path: str
    trendyol_cat_id: Optional[str] = None
    is_leaf: Optional[bool] = False

class CategoryResponse(CategoryBase):
    id: int
    parent_id: Optional[int] = None

# ----------------- PRODUCT SCHEMAS -----------------
class ProductBase(BaseModel):
    name: str
    trendyol_id: Optional[str] = None
    category_id: Optional[int] = None
    brand: Optional[str] = None
    gender: Optional[str] = None
    color: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    rating: Optional[float] = None
    rating_count: Optional[int] = None
    review_count: Optional[int] = None
    images: Optional[Any] = None # JSONB field
    attributes: Optional[Any] = None # JSONB field
    product_url: Optional[str] = None

class ProductResponse(ProductBase):
    id: int

# ----------------- REVIEW SCHEMAS -----------------
class ReviewBase(BaseModel):
    product_id: int
    review_date: Optional[date] = None
    author: Optional[str] = None
    rating: Optional[int] = None
    review_text: Optional[str] = None

class ReviewResponse(ReviewBase):
    id: int
