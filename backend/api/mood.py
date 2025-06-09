from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime, date
from schemas.mood import MoodCreate, MoodGetting, MoodUpdate
from services.mood import MoodService
from api.auth import get_current_user
from models.user import User
from settings.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/mood", tags=["mood"])

@router.post("/", response_model=MoodGetting)
async def create_mood_entry(
    mood: MoodCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Create a new mood entry."""
    if mood.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only create mood entries for yourself"
        )
    mood_service = MoodService()
    return await mood_service.create_mood(mood, current_user.id, session)

@router.get("/", response_model=List[MoodGetting])
async def get_mood_entries(
    start_date: Optional[date] = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: Optional[date] = Query(None, description="End date in YYYY-MM-DD format"),
    user_id: Optional[int] = Query(None, description="User ID to filter moods"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get mood entries with optional date and user filtering.
    
    Dates should be in YYYY-MM-DD format, for example: 2024-03-14
    """
    if user_id and user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You can only view your own mood entries"
        )
    target_user_id = user_id or current_user.id
    mood_service = MoodService()
    return await mood_service.get_moods(target_user_id, start_date, end_date, session)

@router.get("/statistics", response_model=dict)
async def get_mood_statistics(
    month: Optional[int] = None,
    year: Optional[int] = None,
    user_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get monthly mood statistics."""
    if user_id and user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You can only view your own mood statistics"
        )
    target_user_id = user_id or current_user.id
    mood_service = MoodService()
    return await mood_service.get_statistics(target_user_id, month, year, session)

@router.put("/{mood_id}", response_model=MoodGetting)
async def update_mood_entry(
    mood_id: int,
    mood_update: MoodUpdate,
    user_id: int = Query(..., description="User ID whose mood is being updated"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Update a mood entry.
    
    Requires user_id parameter and only allows updating the mood value.
    """
    if user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You can only update your own mood entries"
        )
    mood_service = MoodService()
    return await mood_service.update_mood(mood_id, mood_update, user_id, session)

@router.delete("/{mood_id}")
async def delete_mood_entry(
    mood_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Delete a mood entry."""
    mood_service = MoodService()
    await mood_service.delete_mood(mood_id, current_user.id, session)
    return {"message": "Mood entry deleted successfully"}

@router.get("/by-date/{target_date}", response_model=List[MoodGetting])
async def get_mood_by_date(
    target_date: date,
    user_id: Optional[int] = Query(None, description="User ID to get moods for"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get all mood entries for a specific date.
    
    Date should be in YYYY-MM-DD format, for example: 2024-03-14
    """
    if user_id and user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You can only view your own mood entries"
        )
    target_user_id = user_id or current_user.id
    mood_service = MoodService()
    return await mood_service.get_mood_by_date(target_user_id, target_date, session) 