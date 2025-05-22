from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/todolists", tags=["TodoLists"])


def calculate_progress(completed: int, total: int) -> float:
    if total == 0:
        return 0.0
    return round((completed / total) * 100, 2)


@router.get("/", response_model=list[schemas.TodoListRead])
async def read_todolists(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.TodoList).where(models.TodoList.deleted_at.is_(None))
    )
    todolists = result.scalars().all()

    return [
        schemas.TodoListRead(
            id=todo.id,
            title=todo.title,
            completed_count=todo.completed_count,
            total_count=todo.total_count,
            items=[item for item in todo.items if item.deleted_at is None],
            progress=calculate_progress(todo.completed_count, todo.total_count)
        )
        for todo in todolists
    ]


@router.get("/{todolist_id}", response_model=schemas.TodoListRead)
async def get_todolist(todolist_id: int, db: AsyncSession = Depends(get_db)):
    todolist = await db.get(models.TodoList, todolist_id)
    if not todolist or todolist.deleted_at:
        raise HTTPException(status_code=404, detail="TodoList not found")

    return schemas.TodoListRead(
        id=todolist.id,
        title=todolist.title,
        completed_count=todolist.completed_count,
        total_count=todolist.total_count,
        items=[item for item in todolist.items if item.deleted_at is None],
        progress=calculate_progress(todolist.completed_count, todolist.total_count)
    )


@router.post("/", response_model=schemas.TodoListRead)
async def create_todolist(todolist: schemas.TodoListCreate, db: AsyncSession = Depends(get_db)):
    db_todolist = models.TodoList(title=todolist.title)
    db.add(db_todolist)
    await db.commit()
    await db.refresh(db_todolist)

    return schemas.TodoListRead(
        id=db_todolist.id,
        title=db_todolist.title,
        completed_count=0,
        total_count=0,
        items=[],
        progress=0.0
    )


@router.patch("/{todolist_id}")
async def update_todolist(todolist_id: int, update: schemas.TodoListUpdate, db: AsyncSession = Depends(get_db)):
    db_todolist = await db.get(models.TodoList, todolist_id)
    if not db_todolist or db_todolist.deleted_at:
        raise HTTPException(status_code=404, detail="TodoList not found")

    if update.title is not None:
        db_todolist.title = update.title

    await db.commit()
    return {"detail": "TodoList updated"}


@router.delete("/{todolist_id}")
async def delete_todolist(todolist_id: int, db: AsyncSession = Depends(get_db)):
    db_todolist = await db.get(models.TodoList, todolist_id)
    if not db_todolist or db_todolist.deleted_at:
        raise HTTPException(status_code=404, detail="TodoList not found")

    db_todolist.deleted_at = datetime.utcnow()
    await db.commit()
    return {"detail": "TodoList soft-deleted"}
