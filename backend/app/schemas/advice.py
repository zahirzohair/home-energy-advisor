from pydantic import BaseModel, Field


class AdviceResponse(BaseModel):
    recommendations: list[str] = Field(
        ...,
        description="Prioritized list of actionable energy-saving recommendations",
    )
