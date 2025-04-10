from fastapi import FastAPI
from .database import engine, Base
from .routers import example

app = FastAPI()

app.include_router(example.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
