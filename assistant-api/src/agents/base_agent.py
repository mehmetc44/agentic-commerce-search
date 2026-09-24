from core.config import agent_config
from llm import LLMFactory

class BaseAgent:
    def __init__(self, config_key: str):
        if config_key not in agent_config:
            raise ValueError(
                f"'{config_key}' agent_config.yaml içinde bulunamadı.\n"
                f"Mevcut anahtarlar: {list(agent_config.keys())}"
            )

        self.config_key: str  = config_key
        self.config:     dict = agent_config[config_key]
        self.llm              = LLMFactory.create(self.config)


    def get_max_iterations(self) -> int:

        return int(self.config.get("max_iterations", 5))

    def get_tools(self) -> list[str]:

        return self.config.get("tools", [])
