from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from repository.feedback import FeedbackRepository
from schemas.feedback import FeedbackGetting
from models.user import UserRole

class FeedbackService:
    @staticmethod
    async def create_feedback(
        feedback_data: Dict[str, Any],
        session: AsyncSession
    ) -> FeedbackGetting:
        repo = FeedbackRepository(session)
        feedback = await repo.create(feedback_data)
        return FeedbackGetting.from_orm(feedback)

    @staticmethod
    async def get_user_feedback(
        user_id: int,
        session: AsyncSession
    ) -> list[FeedbackGetting]:
        repo = FeedbackRepository(session)
        feedbacks = await repo.get_all_for_user(user_id)
        return [FeedbackGetting.from_orm(f) for f in feedbacks]

    @staticmethod
    async def get_all_feedback(
        status: Optional[str],
        role: Optional[UserRole],
        user_id: Optional[int],
        session: AsyncSession
    ) -> list[FeedbackGetting]:
        repo = FeedbackRepository(session)
        feedbacks = await repo.get_all_filtered(status, role, user_id)
        return [FeedbackGetting.from_orm(f) for f in feedbacks]

    @staticmethod
    async def update_feedback(
        feedback_id: int,
        feedback_update: Dict[str, Any],
        session: AsyncSession
    ) -> Optional[FeedbackGetting]:
        repo = FeedbackRepository(session)
        feedback = await repo.update(feedback_id, feedback_update)
        return FeedbackGetting.from_orm(feedback) if feedback else None

    @staticmethod
    async def delete_feedback(
        feedback_id: int,
        session: AsyncSession
    ) -> bool:
        repo = FeedbackRepository(session)
        return await repo.delete(feedback_id)