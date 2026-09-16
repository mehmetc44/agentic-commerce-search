from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
import json
import psycopg2

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
        products = final_state.get("products", [])
        
        return {
            "analysis": analysis_str,
            "response": response_text,
            "products": products
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "e-commerce"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASS", "admin123"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )

@app.get("/api/v1/categories")
async def get_main_categories():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Sadece ana (level=1) kategorileri alıyoruz
        cursor.execute("SELECT id, name FROM categories WHERE level = 1 ORDER BY name;")
        categories = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return {"data": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/products/category/{category_id}")
async def get_products_by_category(category_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Seçilen kategori ve alt kategorilerindeki ürünleri çekiyoruz (full_path kullanarak)
        cursor.execute("""
            SELECT p.trendyol_id as product_id, p.name as title, p.images as image_url, p.brand, p.color
            FROM products p
            JOIN categories c ON p.category_id = c.id
            WHERE c.full_path LIKE (SELECT full_path FROM categories WHERE id = %s) || '%'
            LIMIT 20;
        """, (category_id,))
        
        products = []
        for row in cursor.fetchall():
            # JSON olarak tutulan imagelerden ilkini parse et
            image_url = ""
            if row[2]:
                try:
                    images = json.loads(row[2])
                    image_url = images[0] if isinstance(images, list) and len(images) > 0 else row[2]
                except:
                    image_url = row[2]
                    
            products.append({
                "product_id": row[0],
                "title": row[1],
                "image_url": image_url,
                "brand": row[3],
                "color": row[4]
            })
            
        cursor.close()
        conn.close()
        return {"data": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount frontend directory for static files (HTML, CSS, JS)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
