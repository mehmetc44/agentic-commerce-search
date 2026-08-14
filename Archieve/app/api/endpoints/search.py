from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
import asyncio
import json
from app.domain.schemas import SearchRequest, SearchResponse
from app.api.dependencies import get_container

router = APIRouter()

@router.post("/search", response_model=SearchResponse, tags=["Search"])
async def perform_search(request: SearchRequest):
    container = get_container()
    try:
        user_query = request.query
        stage1_json = await asyncio.to_thread(container.tokenizer_service.tokenize_user_query, user_query)
        rewritten_query = stage1_json["analysis"]["rewritten_query"]
        matched_ids = await asyncio.to_thread(container.category_matcher.get_matched_category_ids, rewritten_query)
        stage1_json["analysis"]["extracted_filters"]["category_taxonomy"] = matched_ids
        top_products = await asyncio.to_thread(container.product_search.search_products, final_json=stage1_json, max_results=50)
        
        return SearchResponse(
            original_query=stage1_json["analysis"]["original_query"],
            rewritten_query=rewritten_query,
            extracted_filters=stage1_json["analysis"]["extracted_filters"],
            total_found=len(top_products),
            products=top_products
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/ws-search")
async def websocket_search(websocket: WebSocket):
    await websocket.accept()
    container = get_container()
    try:
        while True:
            data = await websocket.receive_text()
            request_data = json.loads(data)
            user_query = request_data.get("query", "")

            if not user_query:
                await websocket.send_json({"type": "error", "message": "Empty query sent."})
                continue

            await websocket.send_json({"type": "log", "message": f"🔍 <b>Stage 1:</b> Analyzing query with Ollama LLM:<br><span class='text-primary'>'{user_query}'</span>"})

            # Stage 1
            stage1_json = await asyncio.to_thread(container.tokenizer_service.tokenize_user_query, user_query)
            rewritten_query = stage1_json["analysis"]["rewritten_query"]
            extracted_filters = stage1_json["analysis"]["extracted_filters"]
            
            await websocket.send_json({"type": "log", "message": f"✅ <b>LLM Output (Vector Query):</b><br><span class='text-success'>'{rewritten_query}'</span><br><br><b>Extracted Filters:</b><br><pre class='bg-light p-1 border mt-1'>{json.dumps(extracted_filters, indent=2, ensure_ascii=False)}</pre>"})
            await websocket.send_json({"type": "log", "message": f"🌲 <b>Stage 2:</b> Category Matching (SentenceTransformers + CrossEncoder) Starting..."})

            # Stage 2
            matched_ids = await asyncio.to_thread(container.category_matcher.get_matched_category_ids, rewritten_query)
            stage1_json["analysis"]["extracted_filters"]["category_taxonomy"] = matched_ids
            
            await websocket.send_json({"type": "log", "message": f"✅ <b>Category IDs passing the 85% threshold:</b> <span class='badge bg-dark'>{matched_ids}</span>"})
            await websocket.send_json({"type": "log", "message": f"🚀 <b>Stage 3:</b> Performing Vector + SQL Filtered Search in Database (pgvector) and Re-ranking with Cross-Encoder..."})

            # Stage 3
            top_products = await asyncio.to_thread(container.product_search.search_products, final_json=stage1_json, max_results=50)
            
            # Intermediate Log
            if top_products:
                top_5_log = "<ul class='mb-0 ps-3 mt-2' style='list-style-type: none; margin-left: 0; padding-left: 0;'>"
                for p in top_products[:5]:
                    top_5_log += f"<li class='mb-1'><span class='badge bg-success' style='width: 45px;'>%{p['cross_encoder_score']:.1f}</span> <small>{p['title']}</small></li>"
                top_5_log += "</ul>"
                await websocket.send_json({"type": "log", "message": f"✅ <b>{len(top_products)} Products Ranked. Top 5 Candidates:</b>{top_5_log}"})
            else:
                await websocket.send_json({"type": "log", "message": f"❌ <b>No suitable products found.</b>"})

            # Final Results
            await websocket.send_json({
                "type": "result",
                "data": {
                    "original_query": stage1_json["analysis"]["original_query"],
                    "rewritten_query": rewritten_query,
                    "extracted_filters": stage1_json["analysis"]["extracted_filters"],
                    "total_found": len(top_products),
                    "products": top_products
                }
            })

    except WebSocketDisconnect:
        pass
    except Exception as e:
        import traceback
        traceback.print_exc()
        try:
            await websocket.send_json({"type": "error", "message": f"System Error: {str(e)}"})
        except:
            pass
