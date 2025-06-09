from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from repository.thought import ThoughtRepository
from schemas.thought import ThoughtGetting, ThoughtCreate, ThoughtUpdate
from fastapi import HTTPException

class ThoughtService:
    @staticmethod
    async def create_thought(
        thought_data: ThoughtCreate,
        user_id: int,
        session: AsyncSession
    ) -> ThoughtGetting:
        repo = ThoughtRepository(session)
        thought = await repo.create(thought_data, user_id)
        return ThoughtGetting.from_orm(thought)

    @staticmethod
    async def get_thoughts(
        user_id: int,
        session: AsyncSession = None
    ) -> List[ThoughtGetting]:
        repo = ThoughtRepository(session)
        thoughts = await repo.get_all_for_user(user_id)
        return [ThoughtGetting.from_orm(t) for t in thoughts]

    @staticmethod
    async def get_thought(
        thought_id: int,
        user_id: int,
        session: AsyncSession
    ) -> ThoughtGetting:
        repo = ThoughtRepository(session)
        thought = await repo.get_by_id(thought_id)
        if not thought:
            raise HTTPException(status_code=404, detail="Thought entry not found")
        if thought.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to view this thought entry")
        return ThoughtGetting.from_orm(thought)

    @staticmethod
    async def update_thought(
        thought_id: int,
        thought_update: ThoughtUpdate,
        user_id: int,
        session: AsyncSession
    ) -> ThoughtGetting:
        repo = ThoughtRepository(session)
        # Проверяем, принадлежит ли запись пользователю
        thought = await repo.get_by_id(thought_id)
        if not thought:
            raise HTTPException(status_code=404, detail="Thought entry not found")
        if thought.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this thought entry")
            
        thought = await repo.update(thought_id, thought_update, user_id)
        if not thought:
            raise HTTPException(status_code=404, detail="Failed to update thought entry")
        return ThoughtGetting.from_orm(thought)

    @staticmethod
    async def delete_thought(
        thought_id: int,
        user_id: int,
        session: AsyncSession
    ) -> bool:
        repo = ThoughtRepository(session)
        # Проверяем, принадлежит ли запись пользователю
        thought = await repo.get_by_id(thought_id)
        if not thought:
            raise HTTPException(status_code=404, detail="Thought entry not found")
        if thought.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this thought entry")
            
        return await repo.delete(thought_id)

    @staticmethod
    async def get_user_tags(
        user_id: int,
        session: AsyncSession
    ) -> List[str]:
        repo = ThoughtRepository(session)
        return await repo.get_user_tags(user_id)