from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Task
from sqlalchemy import select


class TaskRepository:

    __model: Task = Task

    def __init__(self, db: AsyncSession) -> None:
        self.db: AsyncSession = db

    async def create(self, title: str, content: str, project_id: int) -> Task:

        task = Task(title=title, content=content, project_id=project_id)
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)

        return task

    async def get(self, proj_id: int) -> list[Task]:
        q = select(Task).where(Task.project_id == proj_id)
        tasks = await self.db.execute(q)
        res = tasks.scalars().first()
        return res

    async def get_by_id(self, id: int) -> Task | None:
        q = select(self.__model).where(self.__model.id == id)
        task = await self.db.execute(q)
        return task.scalar()
