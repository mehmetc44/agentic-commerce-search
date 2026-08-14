from typing import Dict, Any
from chatbot.agents.base import BaseAgent
from chatbot.prompts.query_analyzer import QUERY_ANALYZER_SYSTEM_PROMPT
from chatbot.core.schemas.query_analyzer import QueryUnderstandingResponse

class QueryAnalyzerAgent(BaseAgent):
    """
    Agent responsible for analyzing the user's intent, expanding the query,
    and extracting filters using a strict Pydantic output schema.
    """
    def __init__(self, temperature: float = 0.0):
        # Initialize BaseAgent which handles ChatOllama configuration
        super().__init__(temperature=temperature)
        self.system_prompt = QUERY_ANALYZER_SYSTEM_PROMPT
        
        # Enforce output schema contract using LangChain's structured output API
        self.structured_llm = self.llm.with_structured_output(QueryUnderstandingResponse)

    def analyze(self, query: str) -> Dict[str, Any]:
        """
        Analyzes the query and returns parsed intent and filters conforming to the schema.
        """
        prompt = f"{self.system_prompt}\n\nACTUAL USER INPUT:\n\"{query}\""
        
        # Invoke the structured model
        response = self.structured_llm.invoke(prompt)
        
        # Return serialized dict matching the schema contract
        return response.model_dump()
