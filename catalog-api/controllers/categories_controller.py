from fastapi import APIRouter, HTTPException
from typing import List
from services.category_service import CategoryService
from models.schemas import CategoryResponse, VectorSearchRequest

router = APIRouter(prefix="/categories", tags=["Categories"])
service = CategoryService()

@router.post("/closest", response_model=List[CategoryResponse])
def get_closest_categories(request: VectorSearchRequest):
    try:
        return service.get_closest_categories(request.vector, request.limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[CategoryResponse])
def get_categories(limit: int = 100):
    try:
        return service.get_categories(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/main", response_model=List[CategoryResponse])
def get_main_categories(limit: int = 100):
    try:
        return service.get_main_categories(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int):
    try:
        category = service.get_category(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
