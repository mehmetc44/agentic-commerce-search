from enum import Enum

class LLMProvider(str, Enum):
    """Desteklenen LLM sağlayıcıları."""
    DEEPSEEK = "deepseek"
    OLLAMA = "ollama"
    OPENAI = "openai"
