from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from settings.base import Base

class ThoughtRecord(Base):
    __tablename__ = "thought_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    situation: Mapped[str] = mapped_column(Text, nullable=False)
    thought: Mapped[str] = mapped_column(Text, nullable=False)
    emotion: Mapped[str] = mapped_column(Text, nullable=False)
    behavior: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())

    # Relationships
    user = relationship("User", back_populates="thought_records")