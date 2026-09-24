import os
from core.config import agent_config
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

class BaseAgent:
    def __init__(self, config_key: str):
        if config_key not in agent_config:
            raise ValueError(
                f"'{config_key}' agent_config.yaml içinde bulunamadı.\n"
                f"Mevcut anahtarlar: {list(agent_config.keys())}"
            )

        self.config_key: str  = config_key
        self.config:     dict = agent_config[config_key]
        self.llm              = self._init_llm()

    def _init_llm(self):
        """YAML ayarlarını okuyup LangChain model nesnesini döner."""
        provider    = self.config.get("provider", "deepseek").lower()
        model       = self.config.get("model", "deepseek-chat")
        temperature = float(self.config.get("temperature", 0.3))
        max_tokens  = int(self.config.get("max_tokens", 1024))
        timeout     = float(self.config.get("timeout_seconds", 30))

        if provider == "deepseek":
            api_key = os.getenv("DEEPSEEK_API_KEY", "")
            base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
            return ChatOpenAI(
                model=model,
                api_key=api_key,
                base_url=base_url,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=timeout,
            )
            
        elif provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY", "")
            return ChatOpenAI(
                model=model,
                api_key=api_key,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=timeout,
            )
            
        elif provider == "ollama":
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            return ChatOllama(
                model=model,
                base_url=base_url,
                temperature=temperature,
                timeout=timeout,
                options={"num_ctx": 4096, "keep_alive": "24h"},
            )
            
        else:
            raise ValueError(f"Desteklenmeyen LLM provider: '{provider}'. (Geçerli: deepseek, openai, ollama)")

    def get_max_iterations(self) -> int:
        return int(self.config.get("max_iterations", 5))
