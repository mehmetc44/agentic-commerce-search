

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from .BaseLLM import BaseLLM

load_dotenv()

DEEPSEEK_BASE_URL = "https://api.deepseek.com"


class DeepseekLLM(BaseLLM):


    def build(self):
        api_key = os.getenv("DEEPSEEK_API_KEY", "")
        if not api_key:
            raise EnvironmentError(
                "DEEPSEEK_API_KEY bulunamadı.\n"
                ".env dosyasına DEEPSEEK_API_KEY=sk-... satırını ekleyin."
            )

        base_url = os.getenv("DEEPSEEK_BASE_URL", DEEPSEEK_BASE_URL)

        return ChatOpenAI(
            model=self.model,
            api_key=api_key,
            base_url=base_url,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            timeout=self.timeout,
        )
