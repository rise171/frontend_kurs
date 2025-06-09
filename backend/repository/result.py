from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.result import Result
from schemas.result import ResultCreate, ResultUpdate

class ResultRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, result_data: ResultCreate) -> Result:
        result = Result(**result_data.model_dump())
        self.session.add(result)
        await self.session.commit()
        await self.session.refresh(result)
        return result

    async def get_by_id(self, result_id: int) -> Optional[Result]:
        query = select(Result).where(Result.id == result_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_user(self, user_id: int) -> List[Result]:
        query = select(Result).where(Result.user_id == user_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_test(self, test_id: int) -> List[Result]:
        query = select(Result).where(Result.test_id == test_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update(self, result_id: int, result_update: ResultUpdate) -> Optional[Result]:
        result = await self.get_by_id(result_id)
        if not result:
            return None

        update_data = result_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(result, key, value)

        await self.session.commit()
        await self.session.refresh(result)
        return result

    async def delete(self, result_id: int) -> bool:
        result = await self.get_by_id(result_id)
        if not result:
            return False

        await self.session.delete(result)
        await self.session.commit()
        return True