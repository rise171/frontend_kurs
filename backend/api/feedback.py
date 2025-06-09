from fastapi import APIRouter, Depends, HTTPException
from typing import List
from schemas.feedback import FeedbackCreate, FeedbackGetting, FeedbackUpdate
from services.feedback import FeedbackService
from api.auth import get_current_user, get_admin_user
from models.user import User, UserRole
from sqlalchemy.ext.asyncio import AsyncSession
from settings.database import get_session

router = APIRouter(prefix="/feedback", tags=["feedback"])

@router.post("/", response_model=FeedbackGetting)
async def create_feedback(
    feedback_data: FeedbackCreate,
    current_user: User = Depends(get_current_user),
    feedback_service: FeedbackService = Depends(),
    session: AsyncSession = Depends(get_session)
):
    """Create a new feedback."""
    # Verify that the user can only create feedback for themselves
    if feedback_data.user_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="You can only create feedback for your own account"
        )
    
    # Создаем словарь с данными фидбека, включая ID и роль пользователя
    feedback_dict = {
        "message": feedback_data.message,
        "user_id": feedback_data.user_id,
        "user_role": feedback_data.user_role,
        "status": "pending"
    }
    return await feedback_service.create_feedback(feedback_dict, session)

@router.get("/my", response_model=List[FeedbackGetting])
async def get_user_feedback(
    user_id: int,
    current_user: User = Depends(get_current_user),
    feedback_service: FeedbackService = Depends(),
    session: AsyncSession = Depends(get_session)
):
    """Get user's feedback history."""
    # Verify that users can only view their own feedback unless they're admin
    if user_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="You can only view your own feedback"
        )
    return await feedback_service.get_user_feedback(user_id, session)

@router.get("/admin", response_model=List[FeedbackGetting])
async def get_all_feedback(
    status: str = None,
    role: UserRole = None,
    user_id: int = None,
    current_user: User = Depends(get_admin_user),
    feedback_service: FeedbackService = Depends(),
    session: AsyncSession = Depends(get_session)
):
    """Get all feedback (admin only)."""
    return await feedback_service.get_all_feedback(status, role, user_id, session)

@router.put("/{feedback_id}", response_model=FeedbackGetting)
async def update_feedback(
    feedback_id: int,
    feedback_update: FeedbackUpdate,
    current_user: User = Depends(get_admin_user),
    feedback_service: FeedbackService = Depends(),
    session: AsyncSession = Depends(get_session)
):
    """Update feedback status and response (admin only)."""
    return await feedback_service.update_feedback(feedback_id, feedback_update, session)

@router.delete("/{feedback_id}")
async def delete_feedback(
    feedback_id: int,
    current_user: User = Depends(get_admin_user),
    feedback_service: FeedbackService = Depends(),
    session: AsyncSession = Depends(get_session)
):
    """Delete feedback (admin only)."""
    await feedback_service.delete_feedback(feedback_id, session)
    return {"message": "Feedback deleted successfully"} 