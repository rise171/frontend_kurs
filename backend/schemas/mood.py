from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from enum import Enum

class MoodType(str, Enum):
    ANGER = 'anger'
    ANXIETY = 'anxiety'
    SADNESS = 'sadness'
    HAPPINESS = 'happiness'
    MELANCHOLY = 'melancholy'

class MoodCreate(BaseModel):
    mood: MoodType
    user_id: int
    date: Optional[datetime] = None

class MoodDelete(BaseModel):
    id: int

class MoodUpdate(BaseModel):
    mood: MoodType  # Теперь обязательное поле, без даты

class MoodGetting(BaseModel):
    id: int
    user_id: int
    mood: MoodType
    date: datetime

    class Config:
        orm_mode = True