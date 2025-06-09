from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from settings.base import Base

class Test(Base):
    __tablename__ = "tests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)  # ID админа, создавшего тест
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    max_score: Mapped[int] = mapped_column(Integer, nullable=False)  # Максимальный балл за тест
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="tests")
    questions = relationship("Question", back_populates="test", cascade="all, delete-orphan")
    results = relationship("Result", back_populates="test", cascade="all, delete-orphan")
    interpretations = relationship("TestInterpretation", back_populates="test", cascade="all, delete-orphan")