from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from models.feedback import Feedback
from models.user import UserRole
from typing import Optional, List, Dict, Any

class FeedbackRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, feedback_data: Dict[str, Any]) -> Feedback:
        feedback = Feedback(**feedback_data)
        self.session.add(feedback)
        await self.session.commit()
        await self.session.refresh(feedback)
        return feedback

    async def get_by_id(self, feedback_id: int) -> Optional[Feedback]:
        result = await self.session.execute(select(Feedback).where(Feedback.id == feedback_id))
        return result.scalars().first()

    async def update(self, feedback_id: int, feedback_data: Dict[str, Any]) -> Optional[Feedback]:
        # Convert Pydantic model to dict if needed and exclude id
        if hasattr(feedback_data, 'model_dump'):
            update_data = {k: v for k, v in feedback_data.model_dump().items() if k != 'id' and v is not None}
        else:
            update_data = {k: v for k, v in feedback_data.items() if k != 'id' and v is not None}

        await self.session.execute(
            update(Feedback)
            .where(Feedback.id == feedback_id)
            .values(**update_data)
        )
        await self.session.commit()
        return await self.get_by_id(feedback_id)

    async def delete(self, feedback_id: int) -> bool:
        feedback = await self.get_by_id(feedback_id)
        if feedback:
            await self.session.delete(feedback)
            await self.session.commit()
            return True
        return False

    async def get_all_for_user(self, user_id: int) -> List[Feedback]:
        result = await self.session.execute(
            select(Feedback).where(Feedback.user_id == user_id).order_by(Feedback.id)
        )
        return result.scalars().all()

    async def get_all_filtered(
        self, 
        status: Optional[str] = None, 
        role: Optional[UserRole] = None,
        user_id: Optional[int] = None
    ) -> List[Feedback]:
        query = select(Feedback)
        
        if status:
            query = query.where(Feedback.status == status)
        if role:
            query = query.where(Feedback.user_role == role)
        if user_id:
            query = query.where(Feedback.user_id == user_id)
            
        query = query.order_by(Feedback.id)
        result = await self.session.execute(query)
        return result.scalars().all()