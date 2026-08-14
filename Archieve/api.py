"""
E-Commerce Hybrid Search - Web API Entry Point
This file serves as the lightweight wrapper to run the FastAPI application.
All application logic, configurations, and routes are encapsulated inside the `app` package.
"""

from app.api.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
