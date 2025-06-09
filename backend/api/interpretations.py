from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from settings.database import get_session
from services.interpretation_service import InterpretationService
from schemas.interpretation import InterpretationCreate, InterpretationUpdate, InterpretationGetting
from api.auth import get_current_user, get_admin_user
from models.user import User

router = APIRouter(
    prefix="/interpretations",
    tags=["interpretations"]
)

@router.post("/", response_model=InterpretationGetting, status_code=status.HTTP_201_CREATED)
async def create_interpretation(
    interpretation: InterpretationCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_admin_user)  # Используем get_admin_user вместо get_current_admin_user
):
    service = InterpretationService(session)
    return await service.create_interpretation(interpretation)

@router.get("/{interpretation_id}", response_model=InterpretationGetting)
async def get_interpretation(
    interpretation_id: int,
    session: AsyncSession = Depends(get_session)
):
    service = InterpretationService(session)
    interpretation = await service.get_interpretation(interpretation_id)
    if not interpretation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interpretation not found"
        )
    return interpretation

@router.get("/test/{test_id}", response_model=List[InterpretationGetting])
async def get_test_interpretations(
    test_id: int,
    session: AsyncSession = Depends(get_session)
):
    service = InterpretationService(session)
    return await service.get_test_interpretations(test_id)

@router.get("/test/{test_id}/score/{score}", response_model=InterpretationGetting)
async def get_interpretation_by_score(
    test_id: int,
    score: int,
    session: AsyncSession = Depends(get_session)
):
    service = InterpretationService(session)
    interpretation = await service.get_interpretation_by_score(test_id, score)
    if not interpretation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No interpretation found for this score"
        )
    return interpretation

@router.put("/{interpretation_id}", response_model=InterpretationGetting)
async def update_interpretation(
    interpretation_id: int,
    interpretation_update: InterpretationUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_admin_user)  # Используем get_admin_user вместо get_current_admin_user
):
    service = InterpretationService(session)
    interpretation = await service.update_interpretation(interpretation_id, interpretation_update)
    if not interpretation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interpretation not found"
        )
    return interpretation

@router.delete("/{interpretation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_interpretation(
    interpretation_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_admin_user)  # Используем get_admin_user вместо get_current_admin_user
):
    service = InterpretationService(session)
    if not await service.delete_interpretation(interpretation_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interpretation not found"
        ) 