import re
from chatbot.core.config import settings
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

def clean_llm_text(text: str) -> str:
    """
    Strips any thinking tags (<think>...</think>) or unwanted commentary from LLM outputs.
    """
    if not text:
        return ""
    cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
    return cleaned

class BaseAgent:
    """
    Base class for all agents in our system.
    Handles the initialization of the shared language model (DeepSeek API / Ollama).
    """
    def __init__(self, temperature: float = 0.4):
        provider = settings.LLM_PROVIDER.lower()
        
        if provider == "ollama":
            self.llm = ChatOllama(
                model=settings.OLLAMA_MODEL,
                base_url=settings.OLLAMA_BASE_URL,
                temperature=temperature,
                timeout=300.0,
                options={
                    "num_ctx": 4096,
                    "keep_alive": "24h",
                },
            )
        else:
            api_key = settings.DEEPSEEK_API_KEY
            if not api_key:
                raise ValueError(
                    "DEEPSEEK_API_KEY is not configured in environment. "
                    "Please set DEEPSEEK_API_KEY in your .env file."
                )
            
            self.llm = ChatOpenAI(
                model=settings.DEEPSEEK_MODEL,
                openai_api_key=api_key,
                openai_api_base=settings.DEEPSEEK_BASE_URL,
                temperature=temperature,
            )
