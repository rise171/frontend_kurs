from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from schemas.thought import ThoughtCreate, ThoughtGetting, ThoughtUpdate
from services.though import ThoughtService
from api.auth import get_current_user
from models.user import User
from settings.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/thoughts")

@router.post("/", response_model=ThoughtGetting)
async def create_thought_entry(
    thought: ThoughtCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    thought_service: ThoughtService = Depends()
):
    """Create a new thought diary entry."""
    if thought.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only create thought entries for yourself"
        )
    return await thought_service.create_thought(thought, current_user.id, session)

@router.get("/", response_model=List[ThoughtGetting])
async def get_thought_entries(
    user_id: int = Query(..., description="User ID to filter thoughts"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    thought_service: ThoughtService = Depends()
):
    """Get thought diary entries for a specific user."""
    if user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You can only view your own thought entries"
        )
    return await thought_service.get_thoughts(user_id, session)

@router.get("/{thought_id}", response_model=ThoughtGetting)
async def get_thought_entry(
    thought_id: int,
    user_id: int = Query(..., description="User ID whose thought is being retrieved"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    thought_service: ThoughtService = Depends()
):
    """Get a specific thought diary entry."""
    if user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You can only view your own thought entries"
        )
    return await thought_service.get_thought(thought_id, user_id, session)

@router.put("/{thought_id}", response_model=ThoughtGetting)
async def update_thought_entry(
    thought_id: int,
    thought_update: ThoughtUpdate,
    user_id: int = Query(..., description="User ID whose thought is being updated"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    thought_service: ThoughtService = Depends()
):
    """Update a thought diary entry."""
    if user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You can only update your own thought entries"
        )
    return await thought_service.update_thought(thought_id, thought_update, user_id, session)

@router.delete("/{thought_id}")
async def delete_thought_entry(
    thought_id: int,
    user_id: int = Query(..., description="User ID whose thought is being deleted"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    thought_service: ThoughtService = Depends()
):
    """Delete a thought diary entry."""
    if user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own thought entries"
        )
    await thought_service.delete_thought(thought_id, user_id, session)
    return {"message": "Thought entry deleted successfully"} 