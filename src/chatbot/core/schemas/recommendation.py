from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class SearchTarget(BaseModel):
    category: str = Field(
        ...,
        description="Target product category or component (e.g., 'tent', 'sleeping_bag', 'backpack')."
    )
    search_query: str = Field(
        ...,
        description="Semantic search query designed for vector/database retrieval by Extractor Agent."
    )
    filters: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional filter parameters like budget constraints, capacity, season, etc."
    )

class RecommendationOutput(BaseModel):
    action: str = Field(
        ...,
        description="Determines next step: 'search_products' (proceed to Extractor Agent) or 'ask_clarification' (prompt user via Chat Agent)."
    )
    implicit_need_summary: str = Field(
        ...,
        description="Summary of the user's underlying scenario, need, or lifestyle context."
    )
    reasoning: str = Field(
        ...,
        description="Explanation of why this specific solution structure or product combination was recommended."
    )
    search_targets: List[SearchTarget] = Field(
        default_factory=list,
        description="List of specific product categories and semantic search queries for Extractor Agent."
    )
    clarification_question: Optional[str] = Field(
        default=None,
        description="Question to ask user if action is 'ask_clarification'."
    )

class RecommendationResponse(BaseModel):
    recommendation: RecommendationOutput = Field(
        ...,
        description="Structured recommendation response from Recommendation Agent."
    )
