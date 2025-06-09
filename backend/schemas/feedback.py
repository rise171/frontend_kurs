from pydantic import BaseModel
from typing import Optional
from models.user import UserRole

class FeedbackCreate(BaseModel):
    message: str
    user_id: int
    user_role: UserRole

class FeedbackDelete(BaseModel):
    id: int

class FeedbackUpdate(BaseModel):
    id: int
    status: Optional[str] = None
    response: Optional[str] = None

class FeedbackGetting(BaseModel):
    id: int
    user_id: int
    message: str
    status: str
    response: Optional[str] = None
    user_role: UserRole

    class Config:
        orm_mode = True