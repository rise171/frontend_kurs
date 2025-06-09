from fastapi import APIRouter, Depends, HTTPException
from typing import List
from schemas.question import QuestionGetting
from services.question import QuestionService
from api.auth import get_current_user, get_admin_user
from models.user import User
from settings.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/questions", tags=["questions"])

@router.get("/{question_id}", response_model=QuestionGetting)
async def get_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get question by ID."""
    question = await QuestionService.get_question(question_id, session)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.get("/test/{test_id}", response_model=List[QuestionGetting])
async def get_test_questions(
    test_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get all questions for a specific test."""
    questions = await QuestionService.get_test_questions(test_id, session)
    return questions

@router.get("/test/{test_id}/question/{question_id}", response_model=QuestionGetting)
async def get_test_question(
    test_id: int,
    question_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get specific question from a test."""
    question = await QuestionService.get_test_question(test_id, question_id, session)
    return question 