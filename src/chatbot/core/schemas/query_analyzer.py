from typing import Any, Optional
from pydantic import BaseModel, Field

class PriceConstraint(BaseModel):
    min: Optional[float] = Field(
        default=None,
        description="Minimum acceptable price explicitly stated by the user."
    )
    max: Optional[float] = Field(
        default=None,
        description="Maximum acceptable price explicitly stated by the user."
    )

class QueryConstraints(BaseModel):
    price: Optional[PriceConstraint] = Field(
        default=None,
        description="Explicit budget or price constraints."
    )
    attributes: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Other explicit product constraints such as color, size, "
            "brand, technical requirements, waterproofing, compatibility, etc."
        )
    )

class QueryPreferences(BaseModel):
    priorities: list[str] = Field(
        default_factory=list,
        description=(
            "Only explicitly stated user priorities. "
            "Do not convert constraints into priorities."
        )
    )
    attributes: dict[str, Any] = Field(
        default_factory=dict,
        description="Other non-mandatory user preferences."
    )

class RecipientInfo(BaseModel):
    relationship: Optional[str] = Field(
        default=None,
        description="Relationship between the user and the recipient."
    )
    attributes: dict[str, Any] = Field(
        default_factory=dict,
        description="Relevant information about the recipient."
    )

class QueryUnderstanding(BaseModel):
    intent: str = Field(
        description=(
            "The primary shopping or conversation intent, such as conversation, "
            "product_search, gift_recommendation, comparison, compatibility_search, "
            "or decision_support."
        )
    )
    actual_goal: str = Field(
        description="What the user ultimately wants to accomplish."
    )
    relevant_product_category: Optional[str] = Field(
        default=None,
        description=(
            "General product category mentioned or implied by the user. "
            "Do not map it to the catalog taxonomy."
        )
    )
    explicit_constraints: QueryConstraints = Field(
        default_factory=QueryConstraints,
        description="Constraints explicitly stated by the user."
    )
    user_preferences: QueryPreferences = Field(
        default_factory=QueryPreferences,
        description="User preferences and explicitly stated priorities."
    )
    contextual_info: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Additional contextual information such as occasion, "
            "use case, background, or circumstances. "
            "Do not duplicate information represented elsewhere."
        )
    )
    recipient_info: RecipientInfo = Field(
        default_factory=RecipientInfo,
        description=(
            "Information about the intended recipient when shopping "
            "for another person."
        )
    )

class QueryUnderstandingResponse(BaseModel):
    analysis: QueryUnderstanding = Field(
        ...,
        description="Wrapper containing the detailed query understanding analysis."
    )
