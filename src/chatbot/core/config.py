import os
from dotenv import load_dotenv

# Load env variables from .env file
load_dotenv()

class Settings:
    """
    Project settings loaded from environment variables.
    """
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "deepseek")
    
    # DeepSeek API Settings
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    
    # Ollama Settings (Optional)
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen3.5:4b")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

settings = Settings()
