import os

class Settings:
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL_NAME: str = "llama3.2"
    OLLAMA_TIMEOUT: int = 60
    LLM_TEMPERATURE: float = 0.35

    # Veritabanı Ayarları
    DB_PARAMS: dict = {
        "dbname": os.getenv("DB_NAME", "e-commerce"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "admin123"),
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", 5432))
    }

    # Fine-Tuned Model Yolları
    EMBEDDING_MODEL_PATH: str = "sentence-transformers/all-MiniLM-L6-v2"
    CROSS_ENCODER_PATH: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    
    # Kategori Eşleşme Güven Eşiği (%85)
    CATEGORY_CONFIDENCE_THRESHOLD: float = 20.0

    SYSTEM_INSTRUCTIONS = """You are an expert E-commerce Query Tokenizer and Metadata Extractor.
You must output a JSON object containing an "analysis" node with exactly four fields: "original_query", "summary", "rewritten_query", and "extracted_filters".

STRICT PROCESSING RULES:
1. "summary": Clean, concise, human-readable title (2-4 words max) representing the core product type (e.g., "Winter Boots", "Laptop Sleeve").

2. "rewritten_query": This must be a raw, comma-separated English search string optimized STRICTLY for semantic/vector search. 
CRITICAL RULES FOR REWRITING:
- NO STRUCTURED FILTERS: Absolutely DO NOT include brands (e.g., "Metallica", "Nike"), colors (e.g., "red", "black"), prices/budgets (e.g., "under 100", "cheap"), sizes, or genders. These are handled by metadata.
- NO EXACT REPETITIONS: Do not repeat the same word consecutively.
- SEMANTIC & VISUAL EXPANSION: Imagine the aesthetic, style, and core nature of the user's request. Expand the query with highly descriptive, visual, and contextual attributes that define that specific vibe or product type (e.g., If the user wants a "Metallica t-shirt", infer the subculture/style and expand to: "graphic tee, rock band t-shirt, heavy metal merchandise, skull print, vintage wash, comfortable cotton apparel").
- Focus on materials, print types, style genres, and usage contexts that enhance vector similarity.

3. "extracted_filters": Extract shopping filters explicitly mentioned or strongly implied:
   - "brand": Brand or distinct entity name if mentioned (e.g., "Metallica", "Nike"). If none, set to null.
   - "color": Array of colors if mentioned (e.g., ["red"]). If none, set to null.
   - "max_price": Extract maximum financial threshold as a pure integer/number. If none, set to null.
   - "min_price": Extract minimum limit as a pure integer/number if mentioned. If none, set to null.
   - "category_taxonomy": Always set this exact field to an empty array []. DO NOT try to guess the category here.

4. Output MUST be ONLY the raw JSON object. No markdown, no conversation."""

settings = Settings()
