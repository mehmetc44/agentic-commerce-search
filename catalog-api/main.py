from fastapi import FastAPI
from context.DBContext import DBContext
from controllers.categories_controller import router as categories_router
from controllers.products_controller import router as products_router
from controllers.reviews_controller import router as reviews_router
from contextlib import asynccontextmanager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up Catalog API...")
    DBContext.initialize()
    yield
    # Shutdown
    logger.info("Shutting down Catalog API...")
    DBContext.close_all()

app = FastAPI(
    title="AgenticCommerce Catalog API",
    description="Katmanlı mimariye (N-Tier) sahip temiz Catalog API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(categories_router)
app.include_router(products_router)
app.include_router(reviews_router)

@app.get("/")
def read_root():
    return {"message": "Catalog API başarıyla çalışıyor! (Temiz N-Tier Mimari)"}
