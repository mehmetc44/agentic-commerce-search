from fastapi import APIRouter, Query
from backend.services.pipeline import ProductPipeline

router = APIRouter()

# Pipeline objesini başlat
pipeline = ProductPipeline(
    categories_path="data/amazon_categories.csv",
    products_path="data/amazon_products.csv"
)

@router.get("/search")
def search_products(query: str = Query(..., min_length=3)):
    products = pipeline.run(query)
    return {
        "query": query,
        "count": len(products),
        "data": [p.dict() for p in products]
    }