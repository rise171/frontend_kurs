from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from repository.result import ResultRepository
from schemas.result import ResultCreate, ResultUpdate, ResultGetting

class ResultService:
    @staticmethod
    async def create_result(
        result_data: ResultCreate,
        session: AsyncSession
    ) -> ResultGetting:
        repo = ResultRepository(session)
        result = await repo.create(result_data)
        return ResultGetting.model_validate(result)

    @staticmethod
    async def get_result(
        result_id: int,
        session: AsyncSession
    ) -> Optional[ResultGetting]:
        repo = ResultRepository(session)
        result = await repo.get_by_id(result_id)
        return ResultGetting.model_validate(result) if result else None

    @staticmethod
    async def get_user_results(
        user_id: int,
        session: AsyncSession
    ) -> List[ResultGetting]:
        repo = ResultRepository(session)
        results = await repo.get_by_user(user_id)
        return [ResultGetting.model_validate(r) for r in results]

    @staticmethod
    async def get_test_results(
        test_id: int,
        session: AsyncSession
    ) -> List[ResultGetting]:
        repo = ResultRepository(session)
        results = await repo.get_by_test(test_id)
        return [ResultGetting.model_validate(r) for r in results]

    @staticmethod
    async def update_result(
        result_id: int,
        result_update: ResultUpdate,
        session: AsyncSession
    ) -> Optional[ResultGetting]:
        repo = ResultRepository(session)
        result = await repo.update(result_id, result_update)
        return ResultGetting.model_validate(result) if result else None

    @staticmethod
    async def delete_result(
        result_id: int,
        session: AsyncSession
    ) -> bool:
        repo = ResultRepository(session)
        return await repo.delete(result_id) 