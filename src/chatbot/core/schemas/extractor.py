from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ExtractedFilters(BaseModel):
    category: Optional[str] = Field(
        default=None,
        description="Canonical product category name."
    )
    brand: Optional[str] = Field(
        default=None,
        description="Brand name if specified."
    )
    color: Optional[List[str]] = Field(
        default=None,
        description="List of colors requested."
    )
    size: Optional[str] = Field(
        default=None,
        description="Product size specification."
    )
    gender: Optional[str] = Field(
        default=None,
        description="Target gender or demographic group."
    )
    min_price: Optional[float] = Field(
        default=None,
        description="Minimum price threshold."
    )
    max_price: Optional[float] = Field(
        default=None,
        description="Maximum price threshold."
    )
    attributes: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional extracted technical specifications or features."
    )

class ExtractorOutput(BaseModel):
    rewritten_query: str = Field(
        ...,
        description="Clean, keyword-rich semantic search query optimized for vector embedding search."
    )
    extracted_filters: ExtractedFilters = Field(
        ...,
        description="Structured database filter criteria extracted from the input."
    )
    search_strategy: str = Field(
        ...,
        description="Selected retrieval strategy: 'exact_filter_match', 'semantic_vector_search', or 'hybrid_search'."
    )
    reasoning: str = Field(
        ...,
        description="Explanation of how query rewriting and attribute extraction were performed."
    )

class ExtractorResponse(BaseModel):
    extraction: ExtractorOutput = Field(
        ...,
        description="Structured output from Extractor Agent."
    )
