from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from repository.interpretation import InterpretationRepository
from schemas.interpretation import InterpretationCreate, InterpretationUpdate, InterpretationGetting

class InterpretationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = InterpretationRepository(session)

    async def create_interpretation(self, interpretation_data: InterpretationCreate) -> InterpretationGetting:
        interpretation = await self.repository.create(interpretation_data)
        return InterpretationGetting.model_validate(interpretation)

    async def get_interpretation(self, interpretation_id: int) -> Optional[InterpretationGetting]:
        interpretation = await self.repository.get_by_id(interpretation_id)
        if interpretation:
            return InterpretationGetting.model_validate(interpretation)
        return None

    async def get_test_interpretations(self, test_id: int) -> List[InterpretationGetting]:
        interpretations = await self.repository.get_by_test(test_id)
        return [InterpretationGetting.model_validate(interp) for interp in interpretations]

    async def get_interpretation_by_score(self, test_id: int, score: int) -> Optional[InterpretationGetting]:
        interpretation = await self.repository.get_by_score(test_id, score)
        if interpretation:
            return InterpretationGetting.model_validate(interpretation)
        return None

    async def update_interpretation(
        self, interpretation_id: int, interpretation_data: InterpretationUpdate
    ) -> Optional[InterpretationGetting]:
        interpretation = await self.repository.update(interpretation_id, interpretation_data)
        if interpretation:
            return InterpretationGetting.model_validate(interpretation)
        return None

    async def delete_interpretation(self, interpretation_id: int) -> bool:
        return await self.repository.delete(interpretation_id) 