from typing import Optional
from pydantic import BaseModel, Field

class IntentAnalysis(BaseModel):
    is_exact_product_named: bool = Field(
        ...,
        description="True if the user explicitly named a specific concrete product, False otherwise."
    )
    exact_product_name: Optional[str] = Field(
        default=None,
        description=(
            "Extract the product name if explicitly mentioned (e.g. 'Nike Air Force 1', 'flashlight'). "
            "If the user says 'something' or the product is ambiguous, set to null."
        )
    )
    reasoning: str = Field(
        ...,
        description="Briefly explain which Tie-Breaker STEP applies and why."
    )
    intent: str = Field(
        ...,
        description="Classified intent: 'product_search', 'product_recommendation', or 'conversation'."
    )
    detailed_goal: str = Field(
        ...,
        description=(
            "A single sentence summarizing the user's need. "
            "If is_exact_product_named is false, DO NOT hallucinate or guess a product name here!"
        )
    )

class IntentAnalysisResponse(BaseModel):
    analysis: IntentAnalysis = Field(
        ...,
        description="Wrapper containing the detailed intent analysis."
    )
