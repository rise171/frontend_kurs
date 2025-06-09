from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime

class ResultBase(BaseModel):
    test_id: int
    user_id: int
    score: int
    answers: Dict[str, int]  # {question_id: selected_option}

class ResultCreate(ResultBase):
    pass

class ResultDelete(BaseModel):
    id: int

class ResultUpdate(BaseModel):
    variant: Optional[str] = None
    score: Optional[int] = None

class ResultGetting(ResultBase):
    id: int
    completed_at: datetime

    class Config:
        from_attributes = True