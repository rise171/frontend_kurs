from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from repository.question import QuestionRepository
from schemas.question import QuestionCreate, QuestionUpdate, QuestionGetting
from fastapi import HTTPException

class QuestionService:
    @staticmethod
    async def create_question(
        question_data: QuestionCreate,
        test_id: int,
        session: AsyncSession
    ) -> QuestionGetting:
        repo = QuestionRepository(session)
        question = await repo.create(question_data)
        return QuestionGetting.model_validate(question)

    @staticmethod
    async def get_question(
        question_id: int,
        session: AsyncSession
    ) -> Optional[QuestionGetting]:
        repo = QuestionRepository(session)
        question = await repo.get_by_id(question_id)
        return QuestionGetting.model_validate(question) if question else None

    @staticmethod
    async def get_test_questions(
        test_id: int,
        session: AsyncSession
    ) -> List[QuestionGetting]:
        repo = QuestionRepository(session)
        questions = await repo.get_by_test(test_id)
        return [QuestionGetting.model_validate(q) for q in questions]

    @staticmethod
    async def get_test_question(
        test_id: int,
        question_id: int,
        session: AsyncSession
    ) -> Optional[QuestionGetting]:
        """Получить конкретный вопрос теста"""
        repo = QuestionRepository(session)
        question = await repo.get_test_question(test_id, question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found in this test")
        return QuestionGetting.model_validate(question)

    @staticmethod
    async def update_question(
        question_id: int,
        question_update: QuestionUpdate,
        session: AsyncSession
    ) -> Optional[QuestionGetting]:
        repo = QuestionRepository(session)
        question = await repo.update(question_id, question_update)
        return QuestionGetting.model_validate(question) if question else None

    @staticmethod
    async def delete_question(
        question_id: int,
        session: AsyncSession
    ) -> bool:
        repo = QuestionRepository(session)
        return await repo.delete(question_id) 