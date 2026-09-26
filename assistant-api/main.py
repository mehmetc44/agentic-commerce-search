"""
AgenticCommerce — AI Servisi (Port: 8000)

Sadece chatbot ve AI endpointlerini içerir.
DB ve ürün/kategori endpointleri catalog-api (Port: 8001) servisine taşındı.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from graph.workflow import AgenticCommerceWorkflow

app = FastAPI(
    title="AgenticCommerce — AI Service",
    description="AI chatbot servisi. DB işlemleri için catalog-api kullanılır.",
    version="2.0.0",
)

# Uygulama ayağa kalkarken graph'ı (ve agent'ları) başlatıyoruz
workflow_engine = AgenticCommerceWorkflow()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    query: str
    context_products: list[dict] = []


@app.get("/health")
async def health():
    return {"status": "ok", "service": "ai-service"}


@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # LangGraph grafiğini (Workflow Engine üzerinden) çalıştır
        final_state = workflow_engine.execute(
            user_query=request.query,
            context_products=request.context_products
        )

        # Şimdilik dönen intent'i test amaçlı görebiliriz
        return {
            "intent": final_state.get("intent", ""),
            "supervisor_reasoning": final_state.get("supervisor_reasoning", ""),
            "response": final_state.get("response", "")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

