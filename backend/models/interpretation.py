from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from settings.base import Base

class TestInterpretation(Base):
    __tablename__ = "test_interpretations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    test_id: Mapped[int] = mapped_column(ForeignKey("tests.id"), nullable=False)
    min_score: Mapped[int] = mapped_column(Integer, nullable=False)  # Минимальный балл для этой интерпретации
    max_score: Mapped[int] = mapped_column(Integer, nullable=False)  # Максимальный балл для этой интерпретации
    title: Mapped[str] = mapped_column(String(200), nullable=False)  # Краткое описание результата
    description: Mapped[str] = mapped_column(Text, nullable=False)  # Подробное описание и рекомендации

    # Relationships
    test = relationship("Test", back_populates="interpretations") 