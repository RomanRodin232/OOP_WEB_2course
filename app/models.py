from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class TodoList(Base):
    __tablename__ = "todolists"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    completed_count = Column(Integer, default=0)
    total_count = Column(Integer, default=0)

    items = relationship("Item", back_populates="todolist")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    done = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)

    todolist_id = Column(Integer, ForeignKey("todolists.id"))
    todolist = relationship("TodoList", back_populates="items")
