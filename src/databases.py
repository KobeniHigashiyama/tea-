from src.base import AsyncSessionLocal, create_db_and_tables

# Dependency для получения асинхронной сессии
async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
