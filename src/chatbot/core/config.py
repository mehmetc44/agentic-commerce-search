import os
from dotenv import load_dotenv

# Load env variables from .env file
load_dotenv()

class Settings:
    """
    Project settings loaded from environment variables.
    """
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")

settings = Settings()
