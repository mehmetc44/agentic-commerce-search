from fastapi import APIRouter, HTTPException
from typing import List
from services.review_service import ReviewService
from models.schemas import ReviewResponse

router = APIRouter(prefix="/reviews", tags=["Reviews"])
service = ReviewService()

@router.get("/product/{product_id}", response_model=List[ReviewResponse])
def get_product_reviews(product_id: int):
    try:
        return service.get_product_reviews(product_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
