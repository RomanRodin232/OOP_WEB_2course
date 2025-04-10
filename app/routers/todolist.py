from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/todolists", tags=["TodoLists"])

@router.post("/", response_model=schemas.TodoListRead)
async def create_todolist(todolist: schemas.TodoListCreate, db: AsyncSession = Depends(get_db)):
    new_list = models.TodoList(**todolist.dict())
    db.add(new_list)
    await db.commit()
    await db.refresh(new_list)
    return new_list

@router.get("/", response_model=list[schemas.TodoListRead])
async def read_todolists(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.TodoList).options())
    return result.scalars().all()

@router.get("/{todolist_id}", response_model=schemas.TodoListRead)
async def read_todolist(todolist_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.get(models.TodoList, todolist_id)
    if not result:
        raise HTTPException(status_code=404, detail="TodoList not found")
    return result

@router.patch("/{todolist_id}", response_model=schemas.TodoListRead)
async def update_todolist(todolist_id: int, patch: schemas.TodoListUpdate, db: AsyncSession = Depends(get_db)):
    todolist = await db.get(models.TodoList, todolist_id)
    if not todolist:
        raise HTTPException(status_code=404, detail="TodoList not found")
    for key, value in patch.dict(exclude_unset=True).items():
        setattr(todolist, key, value)
    await db.commit()
    await db.refresh(todolist)
    return todolist

@router.delete("/{todolist_id}")
async def delete_todolist(todolist_id: int, db: AsyncSession = Depends(get_db)):
    todolist = await db.get(models.TodoList, todolist_id)
    if not todolist:
        raise HTTPException(status_code=404, detail="TodoList not found")
    await db.delete(todolist)
    await db.commit()
    return {"detail": "TodoList deleted"}
