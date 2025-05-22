from datetime import datetime
from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class TodoList(Base):
    __tablename__ = "todolists"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100))
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_count: Mapped[int] = mapped_column(Integer, default=0)
    total_count: Mapped[int] = mapped_column(Integer, default=0)

    items: Mapped[list["Item"]] = relationship(
        back_populates="todolist", cascade="all, delete-orphan"
    )

class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(250))
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    todolist_id: Mapped[int] = mapped_column(ForeignKey("todolists.id"))
    todolist: Mapped["TodoList"] = relationship(back_populates="items")
