from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict
from schemas.test import TestCreate, TestGetting, TestUpdate, TestWithQuestions
from schemas.question import QuestionCreate, QuestionGetting, QuestionUpdate
from schemas.result import ResultCreate, ResultGetting, ResultUpdate
from services.test import TestService
from services.question import QuestionService
from services.result import ResultService
from api.auth import get_current_user, get_admin_user
from models.user import User
from settings.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/tests", tags=["tests"])

# Тесты - CRUD операции (только для админов)
@router.post("/", response_model=TestGetting)
async def create_test(
    test_data: TestCreate,
    current_user: User = Depends(get_admin_user),
    session: AsyncSession = Depends(get_session)
):
    """Create a new test (admin only)."""
    return await TestService.create_test(test_data, current_user.id, session)

@router.get("/", response_model=List[TestGetting])
async def get_all_tests(
    session: AsyncSession = Depends(get_session)
):
    """Get all available tests."""
    return await TestService.get_all_tests(session)

@router.get("/{test_id}", response_model=TestWithQuestions)
async def get_test(
    test_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get test details with questions."""
    test = await TestService.get_test(test_id, session)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return test

@router.put("/{test_id}", response_model=TestGetting)
async def update_test(
    test_id: int,
    test_update: TestUpdate,
    current_user: User = Depends(get_admin_user),
    session: AsyncSession = Depends(get_session)
):
    """Update test details (admin only)."""
    test = await TestService.update_test(test_id, test_update, current_user.id, current_user.role, session)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return test

@router.delete("/{test_id}")
async def delete_test(
    test_id: int,
    current_user: User = Depends(get_admin_user),
    session: AsyncSession = Depends(get_session)
):
    """Delete a test (admin only)."""
    deleted = await TestService.delete_test(test_id, current_user.id, current_user.role, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="Test not found")
    return {"message": "Test deleted successfully"}

# Вопросы - CRUD операции (только для админов)
@router.post("/{test_id}/questions", response_model=QuestionGetting)
async def create_question(
    test_id: int,
    question_data: QuestionCreate,
    current_user: User = Depends(get_admin_user),
    session: AsyncSession = Depends(get_session)
):
    """Add a question to a test (admin only)."""
    return await QuestionService.create_question(question_data, test_id, session)

@router.put("/questions/{question_id}", response_model=QuestionGetting)
async def update_question(
    question_id: int,
    question_update: QuestionUpdate,
    current_user: User = Depends(get_admin_user),
    session: AsyncSession = Depends(get_session)
):
    """Update a question (admin only)."""
    question = await QuestionService.update_question(question_id, question_update, session)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.delete("/questions/{question_id}")
async def delete_question(
    question_id: int,
    current_user: User = Depends(get_admin_user),
    session: AsyncSession = Depends(get_session)
):
    """Delete a question (admin only)."""
    deleted = await QuestionService.delete_question(question_id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question deleted successfully"}

# Прохождение тестов (для всех пользователей)
@router.post("/{test_id}/submit", response_model=ResultGetting)
async def submit_test(
    test_id: int,
    answers: Dict[str, int],
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Submit test answers and get results."""
    return await TestService.submit_test(test_id, current_user.id, answers, session)

@router.get("/results/my", response_model=List[ResultGetting])
async def get_my_results(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get all test results for the current user."""
    return await TestService.get_user_results(current_user.id, session)

# Results routes
@router.post("/results", response_model=ResultGetting)
async def create_result(
    result: ResultCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Create a new result option for a question."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can create result options"
        )
    result_service = ResultService()
    return await result_service.create_result(result, session)

@router.get("/questions/{question_id}/results", response_model=List[ResultGetting])
async def get_results_for_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get all result options for a specific question."""
    result_service = ResultService()
    return await result_service.get_test_results(question_id, session)

@router.get("/results/{result_id}", response_model=ResultGetting)
async def get_result(
    result_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get a specific result option."""
    result_service = ResultService()
    return await result_service.get_result(result_id, session)

@router.put("/results/{result_id}", response_model=ResultGetting)
async def update_result(
    result_id: int,
    result_update: ResultUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Update a result option."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can update result options"
        )
    result_service = ResultService()
    return await result_service.update_result(result_id, result_update, session)

@router.delete("/results/{result_id}")
async def delete_result(
    result_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Delete a result option."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can delete result options"
        )
    result_service = ResultService()
    await result_service.delete_result(result_id, session)
    return {"message": "Result option deleted successfully"}

@router.get("/results/history/{test_id}", response_model=List[ResultGetting])
async def get_test_results_history(
    test_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get history of results for a specific test."""
    result_service = ResultService()
    return await result_service.get_test_results(test_id, session) 