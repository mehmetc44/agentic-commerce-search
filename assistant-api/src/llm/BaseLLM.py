

from abc import ABC, abstractmethod


class BaseLLM(ABC):


    def __init__(self, model: str, temperature: float, max_tokens: int, timeout: float):
        self.model       = model
        self.temperature = temperature
        self.max_tokens  = max_tokens
        self.timeout     = timeout

    @abstractmethod
    def build(self):

        ...
