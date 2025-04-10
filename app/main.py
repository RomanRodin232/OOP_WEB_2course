from fastapi import FastAPI
from .database import engine, Base
from .routers import todolist, item

app = FastAPI()

app.include_router(todolist.router)
app.include_router(item.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
