import asyncio
from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, String, create_engine, text
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

session_factory = sessionmaker(sync_engine)
async_session_factory = async_sessionmaker(async_engine) 

str_256 = Annotated[str, 256]

class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }