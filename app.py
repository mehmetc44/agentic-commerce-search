from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
import json

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from chatbot.graph import app_graph

app = FastAPI(title="AgenticCommerce API", description="API for E-commerce Chatbot")

# Add CORS middleware to allow the frontend to access the API if needed (mostly useful for local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        initial_state = {
            "user_query": request.query,
            "analysis": "",
            "response": ""
        }
        
        # Invoke LangGraph
        final_state = app_graph.invoke(initial_state)
        
        # Retrieve results
        analysis_str = final_state.get("analysis", "")
        response_text = final_state.get("response", "Yanıt oluşturulamadı.")
        
        return {
            "analysis": analysis_str,
            "response": response_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount frontend directory for static files (HTML, CSS, JS)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
