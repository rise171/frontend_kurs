import asyncio
from settings.database import create_tables, delete_tables

async def init_db():
    print("Удаление старых таблиц...")
    await delete_tables()
    print("Создание новых таблиц...")
    await create_tables()
    print("База данных инициализирована!")

if __name__ == "__main__":
    asyncio.run(init_db()) 