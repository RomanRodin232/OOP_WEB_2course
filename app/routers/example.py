from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..models import User

router = APIRouter()

@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM users")
    users = result.fetchall()
    return [dict(row._mapping) for row in users]
