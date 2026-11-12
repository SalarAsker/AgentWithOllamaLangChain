from pydantic import BaseModel, Field
from typing import Literal

# 1. Define the Pydantic Schema with validation rules
class ProductReviewAnalysis(BaseModel):
    product_name: str = Field(
        description="The name or model of the product being reviewed."
    )
    rating: int = Field(
        ge=1, 
        le=5, 
        description="Integer rating assigned by or inferred from the reviewer, strictly between 1 and 5."
    )
    sentiment: Literal["positive", "neutral", "negative"] = Field(
        description="Overall sentiment of the review."
    )
    advantages: list[str] = Field(
        description="List of key pros, benefits, or positive aspects mentioned."
    )
    disadvantages: list[str] = Field(
        description="List of key cons, flaws, or negative aspects mentioned."
    )
    recommended: bool = Field(
        description="True if the reviewer recommends buying the product, otherwise False."
    )