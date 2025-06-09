from pydantic import BaseModel, Field
from typing import Optional

class InterpretationBase(BaseModel):
    test_id: int
    min_score: int = Field(..., ge=0)  # Минимальное значение 0
    max_score: int = Field(..., ge=0)  # Минимальное значение 0
    title: str
    description: str

class InterpretationCreate(InterpretationBase):
    pass

class InterpretationUpdate(BaseModel):
    min_score: Optional[int] = Field(None, ge=0)
    max_score: Optional[int] = Field(None, ge=0)
    title: Optional[str] = None
    description: Optional[str] = None

class InterpretationGetting(InterpretationBase):
    id: int

    class Config:
        from_attributes = True 