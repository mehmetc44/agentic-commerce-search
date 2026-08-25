from chatbot.core.config import settings
from langchain_openai import ChatOpenAI

class BaseAgent:
    """
    Base class for all agents in our system.
    Handles the initialization of the shared language model (OpenRouter / ChatOpenAI).
    """
    def __init__(self, temperature: float = 0.4):
        api_key = settings.NVIDIA_MODEL_KEY or settings.OPENROUTER_API_KEY
        if not api_key:
            raise ValueError(
                "Neither NVIDIA_MODEL_KEY nor OPENROUTER_API_KEY is configured in the environment. "
                "Please configure the key in your .env file."
            )
        
        self.llm = ChatOpenAI(
            model=settings.OPENROUTER_MODEL,
            openai_api_key=api_key,
            openai_api_base=settings.OPENROUTER_BASE_URL,
            temperature=temperature,
            default_headers={
                "HTTP-Referer": "https://github.com/mehmetc44/agentic-commerce-search",
                "X-Title": "Agentic Commerce Search",
            }
        )
