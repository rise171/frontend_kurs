from pydantic import BaseModel
from typing import Optional, List

class QuestionBase(BaseModel):
    sentence: str
    options: List[str]
    correct_option: int
    score: int

class QuestionCreate(QuestionBase):
    test_id: int

class QuestionDelete(BaseModel):
    id: int

class QuestionUpdate(BaseModel):
    sentence: Optional[str] = None
    options: Optional[List[str]] = None
    correct_option: Optional[int] = None
    score: Optional[int] = None

class QuestionGetting(QuestionBase):
    id: int
    test_id: int

    class Config:
        from_attributes = True