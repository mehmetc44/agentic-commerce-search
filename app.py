"""
AgenticCommerce — AI Servisi (Port: 8000)

Sadece chatbot ve AI endpointlerini içerir.
DB ve ürün/kategori endpointleri catalog-api (Port: 8001) servisine taşındı.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from chatbot.graph import app_graph

app = FastAPI(
    title="AgenticCommerce — AI Service",
    description="AI chatbot servisi. DB işlemleri için catalog-api kullanılır.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    query: str


@app.get("/health")
async def health():
    return {"status": "ok", "service": "ai-service"}


@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        initial_state = {
            "user_query": request.query,
            "analysis": "",
            "response": "",
        }

        # LangGraph grafiğini çalıştır
        final_state = app_graph.invoke(initial_state)

        response_text = final_state.get("response", "Yanıt oluşturulamadı.")
        products = final_state.get("products", [])

        return {
            "analysis": final_state.get("analysis", ""),
            "response": response_text,
            "products": products,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Frontend statik dosyaları
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
