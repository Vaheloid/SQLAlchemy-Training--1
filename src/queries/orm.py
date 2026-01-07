from operator import and_

from sqlalchemy import text, insert, inspect, select, func, cast, Integer
from sqlalchemy.orm import aliased

from database import (
    sync_engine,
    async_engine,
    session_factory,
    async_session_factory,
    Base,
)
from models import WorkersORM, ResumesORM, Workload


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
            result = session.execute(query)  # выполняет запрос
            workers = result.scalars().all()
            print(f"{workers=}")

    @staticmethod
    def update_workers(worker_id: int = 2, new_username: str = "Misha"):
        with session_factory() as session:
            worker_michael = session.get(WorkersORM, worker_id)
            worker_michael.username = new_username
            session.refresh(worker_michael)
            session.commit()

    @staticmethod
    def insert_resumes():
        with session_factory() as session:
            resume_jack_1 = ResumesORM(
                title="Python Junior Developer",
                compensation=50000,
                workload=Workload.fulltime,
                worker_id=1,
            )
            resume_jack_2 = ResumesORM(
                title="Python-разработчик",
                compensation=150000,
                workload=Workload.fulltime,
                worker_id=1,
            )
            resume_michael_1 = ResumesORM(
                title="Python Data Engineer",
                compensation=250000,
                workload=Workload.parttime,
                worker_id=2,
            )
            resume_michael_2 = ResumesORM(
                title="Data Scientist",
                compensation=300000,
                workload=Workload.fulltime,
                worker_id=2,
            )
            session.add_all(
                [resume_jack_1, resume_jack_2, resume_michael_1, resume_michael_2]
            )
            session.commit()
            sync_engine.echo = True

    @staticmethod
    def select_resumes_avg_compensation(like_language: str = "Python"):
        """
        select workload, avg(compensation)::int as avg_compensation
        from resumes
        where title like '%Python%' and compensation > 40000
        group by workload
        """
        with session_factory() as session:
            query = (
                select(
                    ResumesORM.workload,
                    cast(func.avg(ResumesORM.compensation), Integer).label(
                        "avg_compensation"
                    ),
                )
                .select_from(ResumesORM)
                .filter(
                    and_(
                        ResumesORM.title.contains(like_language),
                        ResumesORM.compensation > 40000,
                    )
                )
                .group_by(ResumesORM.workload)
                .having(cast(func.avg(ResumesORM.compensation), Integer) > 70000)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = session.execute(query)
            result = res.all()
            print(result)

    @staticmethod
    def insert_additional_resumes():
        with session_factory() as session:
            workers = [
                {"username": "Artem"},  # id 3
                {"username": "Roman"},  # id 4
                {"username": "Petr"},  # id 5
            ]
            resumes = [
                {
                    "title": "Python программист",
                    "compensation": 60000,
                    "workload": "fulltime",
                    "worker_id": 3,
                },
                {
                    "title": "Machine Learning Engineer",
                    "compensation": 70000,
                    "workload": "parttime",
                    "worker_id": 3,
                },
                {
                    "title": "Python Data Scientist",
                    "compensation": 80000,
                    "workload": "parttime",
                    "worker_id": 4,
                },
                {
                    "title": "Python Analyst",
                    "compensation": 90000,
                    "workload": "fulltime",
                    "worker_id": 4,
                },
                {
                    "title": "Python Junior Developer",
                    "compensation": 100000,
                    "workload": "fulltime",
                    "worker_id": 5,
                },
            ]
            insert_workers = insert(WorkersORM).values(workers)
            insert_resumes = insert(ResumesORM).values(resumes)
            session.execute(insert_workers)
            session.execute(insert_resumes)
            session.commit()

    @staticmethod
    def join_cte_subquery_window_func():
        """
        WITH helper2 AS (
            SELECT *, compensation-avg_workload_compensation AS compensation_diff
            FROM
            (SELECT
                w.id,
                w.username,
                r.compensation,
                r.workload,
                avg(r.compensation) OVER (PARTITION BY workload)::int AS avg_workload_compensation
            FROM resumes r
            JOIN workers w ON r.worker_id = w.id) helper1
        )
        SELECT * FROM helper2
        ORDER BY compensation_diff DESC;
        """
        with session_factory() as session:
            r = aliased(ResumesORM)
            w = aliased(WorkersORM)
            subq = (
                select(
                    r,
                    w,
                    func.avg(r.compensation)
                    .over(partition_by=r.workload)
                    .cast(Integer)
                    .label("avg_workload_compensation"),
                )
                # .select_from(r)
                .join(r, r.worker_id == w.id).subquery("helper1")
            )
            cte = select(
                subq.c.worker_id,
                subq.c.username,
                subq.c.compensation,
                subq.c.workload,
                subq.c.avg_workload_compensation,
                (subq.c.compensation - subq.c.avg_workload_compensation).label(
                    "compensation_diff"
                ),
            ).cte("helper2")
            query = select(cte).order_by(cte.c.compensation_diff.desc())

            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = session.execute(query)
            result = res.all()
            print(result)


class AsyncORM:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def async_insert_workers():
        async with async_session_factory() as session:
            worker_jack = WorkersORM(username="Jack")
            worker_michael = WorkersORM(username="Michael")
            session.add_all([worker_jack, worker_michael])
            await session.commit()
