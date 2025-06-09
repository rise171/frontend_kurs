from sqlalchemy import DateTime, ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from settings.base import Base

class Result(Base):
    __tablename__ = "results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    test_id: Mapped[int] = mapped_column(ForeignKey("tests.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)  # Набранные баллы
    answers: Mapped[dict] = mapped_column(JSON, nullable=False)  # Ответы пользователя на вопросы
    completed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    test = relationship("Test", back_populates="results")
    user = relationship("User", back_populates="test_results")