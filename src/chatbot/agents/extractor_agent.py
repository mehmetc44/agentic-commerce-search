from typing import Dict, Any, Optional
import json
from chatbot.agents.base_agent import BaseAgent
from chatbot.prompts.extractor import EXTRACTOR_SYSTEM_PROMPT
from chatbot.core.schemas.extractor import ExtractorResponse

class ExtractorAgent(BaseAgent):
    """
    Agent responsible for parsing search queries and recommendation targets,
    extracting structured attributes/filters, rewriting queries for semantic vector search,
    and determining the database retrieval strategy.
    """
    def __init__(self, temperature: float = 0.0):
        super().__init__(temperature=temperature)
        self.system_prompt = EXTRACTOR_SYSTEM_PROMPT
        self.structured_llm = self.llm.with_structured_output(ExtractorResponse)

    def extract(self, query: str, context_analysis: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Parses query and intent/recommendation context to extract search parameters.
        """
        ctx_str = ""
        if context_analysis:
            ctx_str = f"\nUPSTREAM CONTEXT:\n{json.dumps(context_analysis, ensure_ascii=False, indent=2)}"

        prompt = (
            f"{self.system_prompt}\n\n"
            f"TARGET SEARCH QUERY / INPUT: \"{query}\"\n"
            f"{ctx_str}"
        )

        response = self.structured_llm.invoke(prompt)
        return response.model_dump()
