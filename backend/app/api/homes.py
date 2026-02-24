import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.messages import HOME_NOT_FOUND, LLM_UNAVAILABLE
from app.schemas.home import HomeCreate, HomeResponse
from app.schemas.advice import AdviceResponse
from app.services.home_service import get_home_by_id, create_home as create_home_record
from app.services.llm_service import LLMProvider, get_llm_provider

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/homes", response_model=HomeResponse)
def create_home(data: HomeCreate, db: Session = Depends(get_db)):
    home = create_home_record(db, data)
    db.commit()
    return HomeResponse.model_validate(home)


@router.get("/homes/{home_id}", response_model=HomeResponse)
def get_home(
    home_id: Annotated[int, Path(ge=1, description="Home ID")],
    db: Session = Depends(get_db),
):
    home = get_home_by_id(db, home_id)
    if not home:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=HOME_NOT_FOUND)
    return HomeResponse.model_validate(home)


@router.post("/homes/{home_id}/advice", response_model=AdviceResponse)
def get_advice(
    home_id: Annotated[int, Path(ge=1, description="Home ID")],
    db: Session = Depends(get_db),
    provider: LLMProvider = Depends(get_llm_provider),
):
    home = get_home_by_id(db, home_id)
    if not home:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=HOME_NOT_FOUND)
    try:
        recommendations = provider.generate_advice(home)
        return AdviceResponse(recommendations=recommendations)
    except Exception as e:
        logger.exception("LLM advice generation failed for home_id=%s", home_id)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=LLM_UNAVAILABLE,
        ) from e
