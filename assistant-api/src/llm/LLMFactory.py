from .BaseLLM import BaseLLM
from .DeepseekLLM import DeepseekLLM
from .OllamaLLM import OllamaLLM
from core.enums import LLMProvider

_REGISTRY: dict[LLMProvider, type[BaseLLM]] = {
    LLMProvider.DEEPSEEK: DeepseekLLM,
    LLMProvider.OLLAMA:   OllamaLLM,
}


class LLMFactory:

    @staticmethod
    def create(config: dict):

        try:
            provider_enum = LLMProvider(config.get("provider", "deepseek").lower())
        except ValueError:
            valid_options = [e.value for e in LLMProvider]
            raise ValueError(
                f"Bilinmeyen LLM provider: '{config.get('provider')}'.\n"
                f"Geçerli seçenekler: {valid_options}"
            )

        model       = config.get("model", "deepseek-chat")
        temperature = float(config.get("temperature", 0.3))
        max_tokens  = int(config.get("max_tokens", 1024))
        timeout     = float(config.get("timeout_seconds", 30))

        if provider_enum not in _REGISTRY:
            raise NotImplementedError(
                f"'{provider_enum.value}' enum olarak tanımlı ancak LLMFactory "
                "içindeki _REGISTRY sözlüğüne sınıfı eklenmemiş!"
            )

        llm_class = _REGISTRY[provider_enum]
        return llm_class(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
        ).build()
