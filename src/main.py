import asyncio
import os
import sys

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from queries.core import SyncCore, AsyncCore
from queries.orm import SyncORM, AsyncORM


async def main():
    SyncORM.create_tables()
    # SyncCore.create_tables()

    SyncORM.insert_workers()
    # SyncCore.create_tables()

    # SyncCore.select_workers()
    # SyncCore.update_workers()

    # SyncORM.select_workers()
    # SyncORM.update_workers()
    SyncORM.insert_resumes()
    SyncORM.insert_additional_resumes()
    # SyncORM.select_resumes_avg_compensation()
    # SyncORM.join_cte_subquery_window_func()
    # SyncORM.select_workers_with_lazy_relationship()
    # SyncORM.select_workers_with_joined_relationship()

    # SyncORM.select_workers_with_selectin_relationship()
    SyncORM.select_workers_with_condition_relationship()
    SyncORM.select_workers_with_condition_relationship_contains_eager()


def create_fast_api_app():
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
    )

    @app.get("/")
    async def index():
        return FileResponse("index.html")

    @app.get("/workers")
    async def get_workers():
        workers = SyncORM.convert_workers_to_dto()
        return workers

    return app


app = create_fast_api_app()
if __name__ == "__main__":
    asyncio.run(main())
    uvicorn.run(app="src.main:app", reload=True)
