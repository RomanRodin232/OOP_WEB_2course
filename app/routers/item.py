from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/", response_model=schemas.ItemRead)
async def create_item(item: schemas.ItemCreate, todolist_id: int, db: AsyncSession = Depends(get_db)):
    new_item = models.Item(**item.dict(), todolist_id=todolist_id)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

@router.get("/", response_model=list[schemas.ItemRead])
async def read_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Item))
    return result.scalars().all()

@router.get("/{item_id}", response_model=schemas.ItemRead)
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await db.get(models.Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.patch("/{item_id}", response_model=schemas.ItemRead)
async def update_item(item_id: int, patch: schemas.ItemUpdate, db: AsyncSession = Depends(get_db)):
    item = await db.get(models.Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in patch.dict(exclude_unset=True).items():
        setattr(item, key, value)
    await db.commit()
    await db.refresh(item)
    return item

@router.delete("/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await db.get(models.Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    await db.delete(item)
    await db.commit()
    return {"detail": "Item deleted"}
