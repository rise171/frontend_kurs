from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from repository.test import TestRepository
from repository.question import QuestionRepository
from repository.result import ResultRepository
from schemas.test import TestGetting, TestCreate, TestUpdate, TestWithQuestions
from schemas.question import QuestionGetting
from schemas.result import ResultGetting, ResultCreate
from fastapi import HTTPException
from models.user import UserRole


class TestService:
    @staticmethod
    async def create_test(
            test_data: TestCreate,
            user_id: int,
            session: AsyncSession
    ) -> TestGetting:
        repo = TestRepository(session)
        test = await repo.create(test_data, user_id)
        return TestGetting.model_validate(test)

    @staticmethod
    async def get_test(
            test_id: int,
            session: AsyncSession
    ) -> Optional[TestWithQuestions]:
        repo = TestRepository(session)
        test = await repo.get_by_id(test_id)
        if not test:
            return None
        
        question_repo = QuestionRepository(session)
        questions = await question_repo.get_by_test(test_id)
        
        test_data = TestWithQuestions(
            **test.__dict__,
            questions=[QuestionGetting.model_validate(q) for q in questions]
        )
        return test_data

    @staticmethod
    async def get_all_tests(
            session: AsyncSession
    ) -> List[TestGetting]:
        repo = TestRepository(session)
        tests = await repo.get_all()
        return [TestGetting.model_validate(t) for t in tests]

    @staticmethod
    async def update_test(
            test_id: int,
            test_update: TestUpdate,
            user_id: int,
            user_role: UserRole,
            session: AsyncSession
    ) -> Optional[TestGetting]:
        if user_role != UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Only admins can update tests")
        
        repo = TestRepository(session)
        test = await repo.update(test_id, test_update)
        return TestGetting.model_validate(test) if test else None

    @staticmethod
    async def delete_test(
            test_id: int,
            user_id: int,
            user_role: UserRole,
            session: AsyncSession
    ) -> bool:
        if user_role != UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Only admins can delete tests")
        
        repo = TestRepository(session)
        return await repo.delete(test_id)

    @staticmethod
    async def submit_test(
            test_id: int,
            user_id: int,
            answers: Dict[str, int],  # {question_id: selected_option}
            session: AsyncSession
    ) -> ResultGetting:
        """Submit test answers and calculate score."""
        repo = TestRepository(session)
        question_repo = QuestionRepository(session)
        result_repo = ResultRepository(session)
        
        # Get test and questions
        test = await repo.get_by_id(test_id)
        if not test:
            raise HTTPException(status_code=404, detail="Test not found")
            
        questions = await question_repo.get_by_test(test_id)
        
        # Calculate score
        total_score = 0
        for question in questions:
            if str(question.id) in answers and answers[str(question.id)] == question.correct_option:
                total_score += question.score
                
        # Create result
        result_data = ResultCreate(
            test_id=test_id,
            user_id=user_id,
            score=total_score,
            answers=answers
        )
        
        result = await result_repo.create(result_data)
        return ResultGetting.model_validate(result)

    @staticmethod
    async def get_user_results(
            user_id: int,
            session: AsyncSession
    ) -> List[ResultGetting]:
        """Get all test results for a user."""
        result_repo = ResultRepository(session)
        results = await result_repo.get_by_user(user_id)
        return [ResultGetting.model_validate(r) for r in results]

    @staticmethod
    async def get_completed_tests_count(
            user_id: int,
            session: AsyncSession
    ) -> int:
        """Get the number of completed tests for a user."""
        result_repo = ResultRepository(session)
        results = await result_repo.get_by_user(user_id)
        return len(results)