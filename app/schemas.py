from pydantic import BaseModel
from typing import List, Optional

class ItemBase(BaseModel):
    title: str
    description: str
    done: bool = False

class ItemCreate(ItemBase): pass

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None

class ItemRead(ItemBase):
    id: int
    todolist_id: int

    class Config:
        orm_mode = True

class TodoListBase(BaseModel):
    title: str

class TodoListCreate(TodoListBase): pass

class TodoListUpdate(BaseModel):
    title: Optional[str] = None

class TodoListRead(TodoListBase):
    id: int
    items: List[ItemRead] = []
    completed_count: int
    total_count: int
    progress: float

    class Config:
        orm_mode = True
