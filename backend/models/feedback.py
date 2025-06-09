from sqlalchemy import Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from settings.base import Base
from models.user import UserRole

class Feedback(Base):
    __tablename__ = "feedbacks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user_role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    message: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Enum('pending', 'resolved', name='feedback_status'), default='pending')
    response: Mapped[str] = mapped_column(Text, nullable=True)

    user = relationship("User", back_populates="feedbacks")