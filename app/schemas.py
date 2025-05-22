from pydantic import BaseModel
from typing import Optional, List


class ItemBase(BaseModel):
    title: str
    content: Optional[str] = None
    done: Optional[bool] = False


class ItemCreate(ItemBase):
    todolist_id: int


class ItemUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    done: Optional[bool]


class ItemRead(ItemBase):
    id: int
    class Config:
        orm_mode = True


class TodoListBase(BaseModel):
    title: str


class TodoListCreate(TodoListBase):
    pass


class TodoListUpdate(BaseModel):
    title: Optional[str]


class TodoListRead(TodoListBase):
    id: int
    completed_count: int
    total_count: int
    progress: float
    items: List[ItemRead]

    class Config:
        orm_mode = True
