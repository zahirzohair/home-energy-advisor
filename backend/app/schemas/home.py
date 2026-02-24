from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.home import HeatingType, InsulationLevel


class HomeCreate(BaseModel):
    size_sqm: int = Field(..., ge=1, le=10000, description="Living area in square metres")
    year_built: Optional[int] = Field(None, ge=1800, le=2026)
    heating_type: HeatingType
    insulation: Optional[InsulationLevel] = None
    notes: Optional[str] = Field(None, max_length=2000)


class HomeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    size_sqm: int
    year_built: Optional[int]
    heating_type: HeatingType
    insulation: Optional[InsulationLevel]
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
