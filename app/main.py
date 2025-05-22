from fastapi import FastAPI
from dotenv import load_dotenv
from app.database import engine
from app.models import Base
from app.api import todolist  # Импортируем маршруты

load_dotenv()  # Загружаем переменные окружения из .env

app = FastAPI(
    title="TodoList CQRS API",
    version="1.0.0"
)

# Подключаем маршруты
app.include_router(todolist.router)

# Создание таблиц (опционально, если не используешь Alembic)
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
