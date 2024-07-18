import datetime

from sqlalchemy import Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List


class Base(DeclarativeBase):
    pass


class Session(Base):
    __tablename__ = "session"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime)
    page_token: Mapped[int]
    backup_type: Mapped[str]
    changes: Mapped[List["Change"]] = relationship(
        back_populates="session"
    )


class Change(Base):
    __tablename__ = "change"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_metadata: Mapped[str] = mapped_column(JSON)
    session_id: Mapped[int] = mapped_column(ForeignKey("session.id", ondelete="CASCADE"), nullable=False)
    file_ref: Mapped[str]
    parent_id: Mapped[str]
    name: Mapped[str]
    is_removed: Mapped[bool]
    file_id: Mapped[str]
    size: Mapped[int]

    session: Mapped["Session"] = relationship(
        back_populates="changes"
    )
