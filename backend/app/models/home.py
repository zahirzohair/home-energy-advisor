import enum
from sqlalchemy import Column, DateTime, Enum, Integer, String, Text
from sqlalchemy.sql import func

from app.core.database import Base


class HeatingType(str, enum.Enum):
    GAS = "GAS"
    OIL = "OIL"
    ELECTRIC = "ELECTRIC"
    HEAT_PUMP = "HEAT_PUMP"
    DISTRICT = "DISTRICT"


class InsulationLevel(str, enum.Enum):
    NONE = "NONE"
    PARTIAL = "PARTIAL"
    GOOD = "GOOD"
    EXCELLENT = "EXCELLENT"


class Home(Base):
    __tablename__ = "homes"

    id = Column(Integer, primary_key=True, index=True)
    size_sqm = Column(Integer, nullable=False)
    year_built = Column(Integer, nullable=True)
    heating_type = Column(Enum(HeatingType), nullable=False)
    insulation = Column(Enum(InsulationLevel), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Home(id={self.id}, size_sqm={self.size_sqm})>"
