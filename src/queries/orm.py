from sqlalchemy import text, insert
from database import sync_engine, async_engine, session_factory, async_session_factory, Base
from models import WorkersORM

def create_tables():
    Base.metadata.drop_all(sync_engine)
    sync_engine.echo = True
    Base.metadata.create_all(sync_engine)
    sync_engine.echo = True

def insert_data():
    with session_factory() as session:
        worker_bobr = WorkersORM(username="Bobr")
        worker_volk = WorkersORM(username="Volk")
        session.add_all([worker_bobr, worker_volk])
        session.commit()

async def async_insert_data():
    async with async_session_factory() as session:
        worker_bobr = WorkersORM(username="Bobr")
        worker_volk = WorkersORM(username="Volk")
        session.add_all([worker_bobr, worker_volk])
        await session.commit()