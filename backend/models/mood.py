from sqlalchemy import DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from settings.base import Base

class MoodCalendar(Base):
    __tablename__ = "mood_calendar"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    mood: Mapped[str] = mapped_column(Enum('anger', 'anxiety', 'sadness', 'happiness', 'melancholy', name='mood_types'))
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="mood_entries")