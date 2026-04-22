from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.routes.search import router as search_router
from backend.routes.product import router as product_router

app = FastAPI()

# CORS middleware (frontend’den API’ye istek için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme aşamasında her porttan gelen isteğe izin verir
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE vb. hepsine izin ver
    allow_headers=["*"],
)

# Frontend klasörünü statik dosya olarak mount et
# html=True => / isteğinde otomatik index.html açılır

# API routerları
# Rotaları uygulamaya dahil etme (sende nasılsa öyle kalsın)
app.include_router(search_router)
app.include_router(product_router, prefix="/api")
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
