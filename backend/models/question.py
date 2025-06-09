from sqlalchemy import ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from settings.base import Base

class Question(Base): #модель вопроса
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    test_id: Mapped[int] = mapped_column(ForeignKey("tests.id"), nullable=False)
    sentence: Mapped[str] = mapped_column(Text, nullable=False) #описание вопроса
    options: Mapped[list] = mapped_column(JSON, nullable=False)  # Список вариантов ответа
    correct_option: Mapped[int] = mapped_column(Integer, nullable=False)  # Индекс правильного ответа
    score: Mapped[int] = mapped_column(Integer, nullable=False)  # Количество баллов за правильный ответ

    test = relationship("Test", back_populates="questions")