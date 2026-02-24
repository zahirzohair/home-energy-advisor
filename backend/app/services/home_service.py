from typing import Optional

from sqlalchemy.orm import Session

from app.models.home import Home
from app.schemas.home import HomeCreate


def get_home_by_id(db: Session, home_id: int) -> Optional[Home]:
    return db.query(Home).filter(Home.id == home_id).first()


def create_home(db: Session, data: HomeCreate) -> Home:
    home = Home(
        size_sqm=data.size_sqm,
        year_built=data.year_built,
        heating_type=data.heating_type,
        insulation=data.insulation,
        notes=data.notes,
    )
    db.add(home)
    db.flush()
    return home
