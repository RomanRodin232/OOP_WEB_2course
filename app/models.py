from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class TodoList(Base):
    __tablename__ = "todolists"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100))

    items: Mapped[list["Item"]] = relationship(back_populates="todolist", cascade="all, delete")

class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(250))
    done: Mapped[bool] = mapped_column(Boolean, default=False)

    todolist_id: Mapped[int] = mapped_column(ForeignKey("todolists.id"))
    todolist: Mapped["TodoList"] = relationship(back_populates="items")
