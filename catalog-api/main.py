from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(categories_router)
api_router.include_router(products_router)
api_router.include_router(reviews_router)

app.include_router(api_router)

app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
