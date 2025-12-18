import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text
from config import settings

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=False, #все коммиты буду выводиться
    #pool_size=5 #количество подключений к бд
    #max_overflow=10, #дополнительные подключения
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False, #все коммиты буду выводиться
    #pool_size=5 #количество подключений к бд
    #max_overflow=10, #дополнительные подключения
)

# with sync_engine.connect() as conn:
#     res = conn.execute(text("SELECT 1,2,3 union select 4,5,6"))
#     print(f"{res.first()=}")

async def get_123():
    async with async_engine.connect() as conn:
        res = await conn.execute(text("SELECT 1,2,3 union select 4,5,6"))
        print(f"{res.first()=}")

asyncio.run(get_123())