from typing import Dict, Any
from chatbot.agents.base_agent import BaseAgent
from chatbot.prompts.intent_analyzer import INTENT_ANALYZER_SYSTEM_PROMPT
from chatbot.core.schemas.intent_analyzer import IntentAnalysisResponse

class IntentAnalyzerAgent(BaseAgent):
    """
    Agent responsible for classifying the user's intent into 
    product_search, product_recommendation, or conversation, 
    and generating a detailed_goal summarizing the user's target.
    """
    def __init__(self, temperature: float = 0.0):
        super().__init__(temperature=temperature)
        self.system_prompt = INTENT_ANALYZER_SYSTEM_PROMPT
        self.structured_llm = self.llm.with_structured_output(IntentAnalysisResponse)

    def analyze(self, query: str) -> Dict[str, Any]:
        """
        Analyzes the user's query and returns classified intent and detailed_goal.
        """
        prompt = f"{self.system_prompt}\n\nACTUAL USER INPUT:\n\"{query}\""
        response = self.structured_llm.invoke(prompt)
        return response.model_dump()
