from models.models import Project
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import contains_eager, joinedload

class ProjectRepository:
    __model: Project = Project

    def __init__(self, db: AsyncSession) -> None:
        self.db: AsyncSession = db

    async def create(self, name: str, deskription: str) -> Project:

        project = self.__model(name=name, deskription=deskription)
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def get(self, skip: int, end: int) -> list[Project]:

        # q = select(self.__model).join(self.__model.tasks).options(contains_eager(self.__model.tasks)).limit(end).offset(skip)
        q = select(self.__model).join(self.__model.tasks).options(joinedload(self.__model.tasks)).limit(end).offset(skip)
        projects = await self.db.execute(q)
        res = projects.scalars().unique().all()
        return res

    async def get_by_id(self, id: int) -> Project | None:
        q = select(self.__model).where(self.__model.id == id)
        project = await self.db.execute(q)
        result = project.scalar().first()

        return result
