import requests
from app.core.config import settings

class OllamaClient:
    """Ollama API ile ham HTTP iletişimini yöneten alt seviye istemci."""
    def __init__(self):
        self.generate_url = f"{settings.OLLAMA_BASE_URL}/api/generate"
        self.model_name = settings.OLLAMA_MODEL_NAME
        self.timeout = settings.OLLAMA_TIMEOUT

    def post_generation(self, prompt: str, temperature: float = settings.LLM_TEMPERATURE) -> str:
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": temperature
            }
        }
        try:
            response = requests.post(self.generate_url, json=payload, timeout=self.timeout)
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            raise RuntimeError(f"Ollama HTTP Error: {response.status_code} - {response.text}")
        except requests.exceptions.Timeout:
            raise TimeoutError(f"Ollama read timeout after {self.timeout} seconds. Check VRAM/RAM.")
        except Exception as e:
            raise ConnectionError(f"Failed to connect Ollama service: {str(e)}")
