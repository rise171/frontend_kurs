import asyncio
from settings.database import engine
from settings.base import Base
from models.user import User
from models.mood import MoodCalendar
from models.thought import ThoughtRecord
from models.test import Test
from models.question import Question
from models.result import Result
from models.feedback import Feedback
from models.interpretation import TestInterpretation

async def recreate_db():
    print("Удаление существующих таблиц...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    print("Создание новых таблиц...")
    # Убедимся, что все модели импортированы
    print("Загруженные модели:")
    print(f"- User (columns: {[c.name for c in User.__table__.columns]})")
    print(f"- MoodCalendar (columns: {[c.name for c in MoodCalendar.__table__.columns]})")
    print(f"- ThoughtRecord (columns: {[c.name for c in ThoughtRecord.__table__.columns]})")
    print(f"- Test (columns: {[c.name for c in Test.__table__.columns]})")
    print(f"- Question (columns: {[c.name for c in Question.__table__.columns]})")
    print(f"- Result (columns: {[c.name for c in Result.__table__.columns]})")
    print(f"- Feedback (columns: {[c.name for c in Feedback.__table__.columns]})")
    print(f"- TestInterpretation (columns: {[c.name for c in TestInterpretation.__table__.columns]})")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("База данных успешно пересоздана!")

if __name__ == "__main__":
    asyncio.run(recreate_db()) 