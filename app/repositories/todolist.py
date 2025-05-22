from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models import TodoList, Item
from app.aggregates.todolist import TodoListAggregate

class TodoListRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, todolist_id: int) -> TodoListAggregate:
        todolist = await self.db.get(TodoList, todolist_id)
        if not todolist:
            raise ValueError("TodoList not found")
        return TodoListAggregate(todolist)

    async def save(self, aggregate: TodoListAggregate):
        self.db.add(aggregate.entity)
        await self.db.commit()
        await self.db.refresh(aggregate.entity)

    async def soft_delete(self, aggregate: TodoListAggregate):
        aggregate.mark_deleted()
        await self.save(aggregate)

    async def recalculate_counts(self, todolist_id: int):
        result = await self.db.execute(
            select(
                func.count().filter(Item.done == True),
                func.count()
            ).where(
                Item.todolist_id == todolist_id,
                Item.deleted_at.is_(None)
            )
        )
        completed, total = result.one()

        todolist = await self.db.get(TodoList, todolist_id)
        if todolist:
            aggregate = TodoListAggregate(todolist)
            aggregate.recalculate_progress(completed, total)
            await self.save(aggregate)
