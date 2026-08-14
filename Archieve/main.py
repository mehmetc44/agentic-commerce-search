"""
E-Commerce Hybrid Search - CLI Testing Wrapper
This file provides a CLI interface to execute and test the semantic search pipeline.
All pipeline orchestration and services are encapsulated inside the `app` package.
"""

from app.services.pipeline import run_hybrid_search_pipeline

if __name__ == "__main__":
    # Test Input Query representing natural language product requests
    test_user_query = "I'm looking for affordable waterproof winter boots for my baby girl, preferably in black or brown, with a budget of no more than 1000 TL"
    
    try:
        run_hybrid_search_pipeline(test_user_query)
    except Exception as e:
        print(f"❌ Sistem Hatası: {str(e)}")