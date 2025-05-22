from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/items", tags=["Items"])


async def recalculate_counts(todolist_id: int, db: AsyncSession):
    result = await db.execute(
        select(models.Item).where(
            models.Item.todolist_id == todolist_id,
            models.Item.deleted_at.is_(None)
        )
    )
    items = result.scalars().all()
    completed = sum(1 for item in items if item.done)
    total = len(items)

    todolist = await db.get(models.TodoList, todolist_id)
    todolist.completed_count = completed
    todolist.total_count = total
    await db.commit()


@router.get("/", response_model=list[schemas.ItemRead])
async def read_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Item).where(models.Item.deleted_at.is_(None))
    )
    items = result.scalars().all()
    return items


@router.post("/", response_model=schemas.ItemRead)
async def create_item(item: schemas.ItemCreate, db: AsyncSession = Depends(get_db)):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    await recalculate_counts(db_item.todolist_id, db)
    return db_item


@router.patch("/{item_id}")
async def update_item(item_id: int, update: schemas.ItemUpdate, db: AsyncSession = Depends(get_db)):
    db_item = await db.get(models.Item, item_id)
    if not db_item or db_item.deleted_at:
        raise HTTPException(status_code=404, detail="Item not found")

    for field, value in update.dict(exclude_unset=True).items():
        setattr(db_item, field, value)

    await db.commit()
    await recalculate_counts(db_item.todolist_id, db)
    return {"detail": "Item updated"}


@router.delete("/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    db_item = await db.get(models.Item, item_id)
    if not db_item or db_item.deleted_at:
        raise HTTPException(status_code=404, detail="Item not found")

    db_item.deleted_at = datetime.utcnow()
    await db.commit()
    await recalculate_counts(db_item.todolist_id, db)
    return {"detail": "Item soft-deleted"}
