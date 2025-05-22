from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import TodoListCreate, TodoListUpdate, TodoListRead
from app.repositories.todolist import TodoListRepository

router = APIRouter(prefix="/todolists", tags=["TodoLists"])


@router.post("/", response_model=TodoListRead)
async def create_todolist(data: TodoListCreate, db: AsyncSession = Depends(get_db)):
    from app.models import TodoList

    todolist = TodoList(title=data.title)
    aggregate = TodoListAggregate(todolist)
    repo = TodoListRepository(db)
    await repo.save(aggregate)

    return TodoListRead(
        id=todolist.id,
        title=todolist.title,
        completed_count=0,
        total_count=0,
        progress=0.0,
        items=[]
    )


@router.patch("/{todolist_id}")
async def update_todolist(todolist_id: int, data: TodoListUpdate, db: AsyncSession = Depends(get_db)):
    repo = TodoListRepository(db)
    aggregate = await repo.get_by_id(todolist_id)

    if data.title:
        aggregate.update_title(data.title)

    await repo.save(aggregate)
    return {"detail": "Updated"}


@router.delete("/{todolist_id}")
async def delete_todolist(todolist_id: int, db: AsyncSession = Depends(get_db)):
    repo = TodoListRepository(db)
    aggregate = await repo.get_by_id(todolist_id)
    await repo.soft_delete(aggregate)
    return {"detail": "Deleted"}
