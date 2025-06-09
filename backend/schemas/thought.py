from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ThoughtBase(BaseModel):
    situation: str
    thought: str
    emotion: str
    behavior: str

class ThoughtCreate(ThoughtBase):
    user_id: int
    date: Optional[datetime] = None

class ThoughtDelete(BaseModel):
    id: int

class ThoughtUpdate(ThoughtBase):
    situation: Optional[str] = None
    thought: Optional[str] = None
    emotion: Optional[str] = None
    behavior: Optional[str] = None

class ThoughtGetting(ThoughtBase):
    id: int
    user_id: int
    date: datetime

    class Config:
        orm_mode = True