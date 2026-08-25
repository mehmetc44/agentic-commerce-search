from typing import Dict, Any, Optional
import json
from chatbot.agents.base_agent import BaseAgent
from chatbot.prompts.recommendation import RECOMMENDATION_SYSTEM_PROMPT
from chatbot.core.schemas.recommendation import RecommendationResponse

class RecommendationAgent(BaseAgent):
    """
    Agent responsible for analyzing implicit user needs and scenario contexts,
    decomposing them into product search goals for Extractor Agent,
    or generating clarification questions via Chat Agent.
    """
    def __init__(self, temperature: float = 0.2):
        super().__init__(temperature=temperature)
        self.system_prompt = RECOMMENDATION_SYSTEM_PROMPT
        self.structured_llm = self.llm.with_structured_output(RecommendationResponse)

    def recommend(self, query: str, intent_analysis: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Processes user query and intent analysis context to generate recommendation strategy.
        """
        analysis_context = ""
        if intent_analysis:
            analysis_context = f"\nINTENT ANALYZER CONTEXT:\n{json.dumps(intent_analysis, ensure_ascii=False, indent=2)}"
            
        prompt = (
            f"{self.system_prompt}\n\n"
            f"USER QUERY: \"{query}\"\n"
            f"{analysis_context}"
        )
        
        response = self.structured_llm.invoke(prompt)
        return response.model_dump()
