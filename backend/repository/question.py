from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.question import Question
from schemas.question import QuestionCreate, QuestionUpdate

class QuestionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, question_data: QuestionCreate) -> Question:
        question = Question(**question_data.model_dump())
        self.session.add(question)
        await self.session.commit()
        await self.session.refresh(question)
        return question

    async def get_by_id(self, question_id: int) -> Optional[Question]:
        query = select(Question).where(Question.id == question_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_test(self, test_id: int) -> List[Question]:
        query = select(Question).where(Question.test_id == test_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_test_question(self, test_id: int, question_id: int) -> Optional[Question]:
        """Получить конкретный вопрос теста"""
        query = select(Question).where(
            Question.test_id == test_id,
            Question.id == question_id
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update(self, question_id: int, question_update: QuestionUpdate) -> Optional[Question]:
        question = await self.get_by_id(question_id)
        if not question:
            return None

        update_data = question_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(question, key, value)

        await self.session.commit()
        await self.session.refresh(question)
        return question

    async def delete(self, question_id: int) -> bool:
        question = await self.get_by_id(question_id)
        if not question:
            return False

        await self.session.delete(question)
        await self.session.commit()
        return True