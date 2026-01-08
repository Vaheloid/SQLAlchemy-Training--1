import datetime
from typing import Optional, Annotated
from sqlalchemy import (
    ForeignKey,
    Table,
    Column,
    Integer,
    String,
    MetaData,
    func,
    text,
    Index,
    CheckConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base, str_256
import enum

metadata_obj = MetaData()

workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
)

intpk = Annotated[int, mapped_column(primary_key=True)]
updated_at = Annotated[
    datetime.datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.utcnow
    ),
]
created_at = Annotated[
    datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]


class WorkersORM(Base):
    __tablename__ = "workers"
    id: Mapped[intpk]
    username: Mapped[str]

    resumes: Mapped[list["ResumesORM"]] = relationship(
        back_populates="worker",
    )
    resumes_parttime: Mapped[list["ResumesORM"]] = relationship(
        back_populates="worker",
        primaryjoin="and_(WorkersORM.id == ResumesORM.worker_id, ResumesORM.workload == 'parttime')",
        order_by="ResumesORM.id.desc()",
    )


class Workload(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"


class ResumesORM(Base):
    __tablename__ = "resumes"
    id: Mapped[intpk]
    title: Mapped[str_256]
    compensation: Mapped[Optional[int]]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    updated_at: Mapped[updated_at]
    created_at: Mapped[created_at]

    worker: Mapped["WorkersORM"] = relationship(
        back_populates="resumes",
    )

    repr_cols_num = 4
    repr_cols = tuple(
        "created_at",
    )

    __table_args__ = (
        Index("title index", "title"),
        CheckConstraint("compensation > 0", name="check_compensation_positive"),
    )
