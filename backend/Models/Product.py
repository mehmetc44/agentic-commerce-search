from typing import Optional
from pydantic import BaseModel

class Product(BaseModel):
    asin: str
    title: str
    imgUrl: str
    productURL: str
    stars: Optional[float]
    reviews: Optional[int]
    price: Optional[float]
    listPrice: Optional[float]
    category_id: int
    isBestSeller: Optional[bool]
    boughtInLastMonth: Optional[int]