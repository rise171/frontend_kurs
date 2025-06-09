from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from schemas.question import QuestionGetting

class TestBase(BaseModel):
    name: str
    description: str
    max_score: int

class TestCreate(TestBase):
    pass

class TestUpdate(TestBase):
    name: Optional[str] = None
    description: Optional[str] = None
    max_score: Optional[int] = None

class TestGetting(TestBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TestWithQuestions(TestGetting):
    questions: List[QuestionGetting]

    class Config:
        from_attributes = True