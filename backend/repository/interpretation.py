from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.interpretation import TestInterpretation
from schemas.interpretation import InterpretationCreate, InterpretationUpdate

class InterpretationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, interpretation_data: InterpretationCreate) -> TestInterpretation:
        interpretation = TestInterpretation(**interpretation_data.model_dump())
        self.session.add(interpretation)
        await self.session.commit()
        await self.session.refresh(interpretation)
        return interpretation

    async def get_by_id(self, interpretation_id: int) -> Optional[TestInterpretation]:
        query = select(TestInterpretation).where(TestInterpretation.id == interpretation_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_test(self, test_id: int) -> List[TestInterpretation]:
        query = select(TestInterpretation).where(TestInterpretation.test_id == test_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_score(self, test_id: int, score: int) -> Optional[TestInterpretation]:
        query = select(TestInterpretation).where(
            TestInterpretation.test_id == test_id,
            TestInterpretation.min_score <= score,
            TestInterpretation.max_score >= score
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update(self, interpretation_id: int, interpretation_update: InterpretationUpdate) -> Optional[TestInterpretation]:
        interpretation = await self.get_by_id(interpretation_id)
        if not interpretation:
            return None

        update_data = interpretation_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(interpretation, key, value)

        await self.session.commit()
        await self.session.refresh(interpretation)
        return interpretation

    async def delete(self, interpretation_id: int) -> bool:
        interpretation = await self.get_by_id(interpretation_id)
        if not interpretation:
            return False

        await self.session.delete(interpretation)
        await self.session.commit()
        return True 