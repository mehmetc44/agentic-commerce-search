import os
from pathlib import Path
import yaml
from dotenv import load_dotenv


_ENV_PATH = Path(__file__).parents[2] / ".env"
load_dotenv(dotenv_path=_ENV_PATH, override=True)


class Settings:


    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")


    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    CATALOG_API_URL: str = os.getenv("CATALOG_API_URL", "http://localhost:8001")
    EMBEDDING_MODEL_PATH: str = os.getenv("EMBEDDING_MODEL_PATH", "../shared/ai-models/embeddings")


settings = Settings()



_CONFIG_PATH = Path(__file__).parents[1] / "config" / "agent_config.yaml"

def _load_agent_config() -> dict:
    if not _CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"agent_config.yaml bulunamadı: {_CONFIG_PATH}\n"
            "Lütfen assistant-api/config/agent_config.yaml dosyasının var olduğundan emin olun."
        )
    with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

agent_config = _load_agent_config()
