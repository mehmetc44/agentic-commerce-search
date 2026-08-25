from chatbot.core.config import settings
from langchain_ollama.chat_models import ChatOllama

class BaseAgent:
    """
    Base class for all agents in our system.
    Handles the initialization of the shared language model (Ollama).
    """
    def __init__(self, temperature: float = 0.4):
        self.llm = ChatOllama(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=temperature
        )
