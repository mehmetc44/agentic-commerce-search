from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.api.dependencies import get_container
from app.api.endpoints.search import router as search_router
from app.api.endpoints.catalog import router as catalog_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize the DI container (loads models and DB connections)
    container = get_container()
    container.initialize()
    yield
    # Shutdown: clean up DB connection resources
    container.close()

app = FastAPI(
    title="E-Commerce Hybrid Search API",
    description="Vector Search + SQL Filters + Cross-Encoder Re-ranking",
    version="1.0.0",
    lifespan=lifespan
)

# Allow CORS for UI access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers under /api/v1 prefix
api_router = APIRouter(prefix="/api/v1")
api_router.include_router(search_router)
api_router.include_router(catalog_router)

app.include_router(api_router)

# Mount static frontend files
# Must be mounted last so that it does not intercept API routes
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
