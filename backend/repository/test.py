from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.test import Test
from schemas.test import TestCreate, TestUpdate
from typing import List, Optional, Dict
from datetime import datetime

class TestRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, test_data: TestCreate, user_id: int) -> Test:
        test = Test(
            user_id=user_id,
            name=test_data.name,
            description=test_data.description,
            max_score=test_data.max_score
        )
        self.session.add(test)
        await self.session.commit()
        await self.session.refresh(test)
        return test

    async def get_by_id(self, test_id: int) -> Optional[Test]:
        result = await self.session.execute(
            select(Test).where(Test.id == test_id)
        )
        return result.scalars().first()

    async def get_all(self) -> List[Test]:
        result = await self.session.execute(select(Test).order_by(Test.id))
        return result.scalars().all()

    async def get_user_results(self, user_id: int) -> List[Test]:
        result = await self.session.execute(
            select(Test).where(Test.user_id == user_id).order_by(Test.created_at.desc())
        )
        return result.scalars().all()

    async def update(self, test_id: int, test_update: TestUpdate) -> Optional[Test]:
        test = await self.get_by_id(test_id)
        if not test:
            return None
        
        update_data = test_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(test, key, value)
        
        await self.session.commit()
        await self.session.refresh(test)
        return test

    async def delete(self, test_id: int) -> bool:
        test = await self.get_by_id(test_id)
        if not test:
            return False

        await self.session.delete(test)
        await self.session.commit()
        return True

    async def count_completed_tests(self, user_id: int) -> int:
        """Count the number of completed tests for a user."""
        result = await self.session.execute(
            select(func.count(Test.id))
            .where(Test.user_id == user_id)
        )
        return result.scalar() or 0

    async def update_result(self, test_id: int, total_score: int) -> Optional[Test]:
        test = await self.session.get(Test, test_id)
        if test:
            test.result = total_score
            await self.session.commit()
            await self.session.refresh(test)
        return test