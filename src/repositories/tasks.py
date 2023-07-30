from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Task
from sqlalchemy import select
from .base import SQLAlchemyRepository


class TaskRepository(SQLAlchemyRepository):

    model: Task = Task

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def get_by_proj_id(self, proj_id: int) -> list[Task]:
        q = select(self.model).where(Task.project_id == proj_id)
        tasks = await self.db.execute(q)
        res = tasks.scalars()

        return res
