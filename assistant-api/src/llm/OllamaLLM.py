

import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from .BaseLLM import BaseLLM

load_dotenv()

OLLAMA_DEFAULT_BASE_URL = "http://localhost:11434"


class OllamaLLM(BaseLLM):


    def build(self):
        base_url = os.getenv("OLLAMA_BASE_URL", OLLAMA_DEFAULT_BASE_URL)

        return ChatOllama(
            model=self.model,
            base_url=base_url,
            temperature=self.temperature,
            timeout=self.timeout,
            options={
                "num_ctx": 4096,
                "keep_alive": "24h",
            },
        )
