from pydantic import BaseModel, Field

class IntentAnalysis(BaseModel):
    intent: str = Field(
        description=(
            "Classified intent: 'product_search' for direct/deterministic search, "
            "'product_recommendation' for implicit need/semantic discovery, "
            "or 'conversation' for chat/Q&A/greetings."
        )
    )
    detailed_goal: str = Field(
        description=(
            "A single English or Turkish sentence summarizing exactly what the user wants, "
            "providing context for the next agent."
        )
    )

class IntentAnalysisResponse(BaseModel):
    analysis: IntentAnalysis = Field(
        ...,
        description="Wrapper containing the intent analysis node."
    )
