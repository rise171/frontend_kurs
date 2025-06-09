from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from models.thought import ThoughtRecord
from schemas.thought import ThoughtCreate, ThoughtUpdate
from typing import Optional, List, Dict, Any
from datetime import datetime

class ThoughtRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, thought_data: ThoughtCreate, user_id: int) -> ThoughtRecord:
        thought = ThoughtRecord(
            user_id=user_id,
            situation=thought_data.situation,
            thought=thought_data.thought,
            emotion=thought_data.emotion,
            behavior=thought_data.behavior,
            date=thought_data.date or datetime.utcnow()
        )
        self.session.add(thought)
        await self.session.commit()
        await self.session.refresh(thought)
        return thought

    async def get_by_id(self, thought_id: int) -> Optional[ThoughtRecord]:
        result = await self.session.execute(
            select(ThoughtRecord).where(ThoughtRecord.id == thought_id)
        )
        return result.scalars().first()

    async def get_all_for_user(
        self,
        user_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[ThoughtRecord]:
        query = select(ThoughtRecord).where(ThoughtRecord.user_id == user_id)
        
        if start_date:
            query = query.where(func.date(ThoughtRecord.date) >= start_date)
        if end_date:
            query = query.where(func.date(ThoughtRecord.date) <= end_date)
            
        query = query.order_by(ThoughtRecord.date.desc())
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(
        self,
        thought_id: int,
        thought_update: ThoughtUpdate,
        user_id: int
    ) -> Optional[ThoughtRecord]:
        thought = await self.get_by_id(thought_id)
        if not thought:
            return None
        
        if thought.user_id != user_id:
            return None
        
        update_data = thought_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(thought, key, value)
        
        await self.session.commit()
        await self.session.refresh(thought)
        return thought

    async def delete(self, thought_id: int) -> bool:
        thought = await self.get_by_id(thought_id)
        if thought:
            await self.session.delete(thought)
            await self.session.commit()
            return True
        return False