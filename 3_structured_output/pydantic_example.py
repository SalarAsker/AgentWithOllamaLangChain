from pydantic import BaseModel, Field
from typing import Literal

class FeedbackAnalysis(BaseModel):
    summary: str = Field(
        min_length=10,
        max_length=200,
        description="A concise summary of the customer feedback."
    )
    sentiment: Literal["positive", "neutral", "negative"] = Field(
        description="The overall sentiment of the feedback."
    )
    problems: list[str] = Field(
        description="A list of problems identified in the feedback."
    )
    follow_up_required: bool = Field(
        description="Whether a follow-up is required."
    )
    severity_dissatisfaction:int = Field(
        ge=1,
        le=5,
        description="The severity of customer dissatisfaction (1-5)."
    )
    severity_satisfaction:int = Field(
        ge=1,
        le=5,
        description="The severity of customer satisfaction (1-5)."
    )