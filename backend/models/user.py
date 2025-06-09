from sqlalchemy import INTEGER, TEXT, VARCHAR, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from settings.base import Base
from enum import Enum as PyEnum


class UserRole(str, PyEnum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    username: Mapped[str] = mapped_column(VARCHAR(50), unique=True, nullable=False)
    login: Mapped[str] = mapped_column(TEXT, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(TEXT, nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER)

    # Relationships
    feedbacks = relationship("Feedback", back_populates="user")
    mood_entries = relationship("MoodCalendar", back_populates="user")
    tests = relationship("Test", back_populates="user")
    thought_records = relationship("ThoughtRecord", back_populates="user")
    test_results = relationship("Result", back_populates="user")