import os
from dotenv import load_dotenv

# Load env variables from .env file
load_dotenv()

class Settings:
    """
    Project settings loaded from environment variables.
    """
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    
    # OpenRouter / Nvidia Model Settings
    NVIDIA_MODEL_KEY: str = os.getenv("NVIDIA_MODEL_KEY", "")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "nvidia/nemotron-3.5-lightning:free")
    OPENROUTER_BASE_URL: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

settings = Settings()
