from typing import Any, List, Optional, Dict
from pydantic import BaseModel, Field

class PriceConstraint(BaseModel):
    min: Optional[float] = Field(
        default=None,
        description="Minimum acceptable price."
    )
    max: Optional[float] = Field(
        default=None,
        description="Maximum acceptable price."
    )

class QueryConstraints(BaseModel):
    price: Optional[PriceConstraint] = Field(
        default=None,
        description="Explicit budget or price constraints."
    )
    attributes: Dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Other explicit product constraints such as color, "
            "size, waterproofing, brand, compatibility requirements, etc."
        )
    )

class QueryPreferences(BaseModel):
    priorities: List[str] = Field(
        default_factory=list,
        description=(
            "Preferences or priorities explicitly stated or strongly "
            "implied by the user."
        )
    )
    attributes: Dict[str, Any] = Field(
        default_factory=dict,
        description="Other relevant user preferences."
    )

class RecipientInfo(BaseModel):
    relationship: Optional[str] = Field(
        default=None,
        description="Relationship between the user and the recipient."
    )
    attributes: Dict[str, Any] = Field(
        default_factory=dict,
        description="Relevant information about the recipient."
    )

class ExtractedFiltersSchema(BaseModel):
    category_taxonomy: List[str] = Field(
        default_factory=list,
        description="Always empty list []"
    )

class QueryUnderstanding(BaseModel):
    primary_shopping_intent: str = Field(
        description=(
            "The primary shopping intent, such as product_search, "
            "gift_recommendation, comparison, compatibility_search, "
            "or decision_support."
        )
    )
    actual_goal: str = Field(
        description="What the user ultimately wants to accomplish."
    )
    relevant_product_category: Optional[str] = Field(
        default=None,
        description=(
            "The general product category mentioned or implied by "
            "the user's request. Do not map it to a specific catalog taxonomy."
        )
    )
    explicit_constraints: QueryConstraints = Field(
        default_factory=QueryConstraints,
        description="Constraints explicitly stated by the user."
    )
    user_preferences: QueryPreferences = Field(
        default_factory=QueryPreferences,
        description="User preferences and priorities relevant to the request."
    )
    contextual_info: Dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Relevant contextual information such as occasion, "
            "use case, background, or circumstances."
        )
    )
    recipient_info: RecipientInfo = Field(
        default_factory=RecipientInfo,
        description=(
            "Information about the intended recipient when the user "
            "is shopping for someone else."
        )
    )
    extracted_filters: ExtractedFiltersSchema = Field(
        default_factory=ExtractedFiltersSchema,
        description="Extracted filters for downstream search service integrations."
    )

class QueryUnderstandingResponse(BaseModel):
    analysis: QueryUnderstanding = Field(
        ...,
        description="Wrapper containing the detailed query understanding analysis."
    )
