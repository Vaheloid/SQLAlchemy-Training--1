import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text
from config import settings

#синхронный движок
sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True, #все коммиты буду выводиться
    #pool_size=5 #количество подключений к бд
    #max_overflow=10, #дополнительные подключения
)
#асинхронный движок
async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True, #все коммиты буду выводиться
    #pool_size=5 #количество подключений к бд
    #max_overflow=10, #дополнительные подключения
)