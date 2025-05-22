from datetime import datetime
from app.models import TodoList

class TodoListAggregate:
    def __init__(self, entity: TodoList):
        self.entity = entity

    def update_title(self, new_title: str):
        self.entity.title = new_title

    def mark_deleted(self):
        self.entity.deleted_at = datetime.utcnow()

    def recalculate_progress(self, completed: int, total: int):
        self.entity.completed_count = completed
        self.entity.total_count = total
