from sqlalchemy import text, insert, inspect, select
from database import sync_engine, async_engine, session_factory, async_session_factory, Base
from models import WorkersORM

class SyncORM:
    @staticmethod
    def create_tables():
        sync_engine.echo = False
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_workers():
        with session_factory() as session:
            worker_jack = WorkersORM(username="Jack")
            worker_michael = WorkersORM(username="Michael")
            session.add_all([worker_jack, worker_michael])
            session.flush()
            session.commit()

    @staticmethod
    def select_workers():
        with session_factory() as session:
            query = select(WorkersORM)
            result = session.execute(query) #выполняет запрос
            workers = result.scalars().all()
            print(f"{workers=}") 

    @staticmethod
    def update_workers(worker_id: int = 2, new_username: str = "Misha"):
        with session_factory() as session:
            worker_michael = session.get(WorkersORM, worker_id)
            worker_michael.username = new_username
            session.refresh(worker_michael)
            session.commit()

async def async_insert_data():
    async with async_session_factory() as session:
        worker_jack = WorkersORM(username="Jack")
        worker_michael = WorkersORM(username="Michael")
        session.add_all([worker_jack, worker_michael])
        await session.commit()

class AsyncORM:
    pass