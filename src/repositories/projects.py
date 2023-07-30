from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import joinedload
from models.models import Project
from .base import SQLAlchemyRepository
import core.exceptions as exceptions


class ProjectRepository(SQLAlchemyRepository):
    model: Project = Project

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def get_list(self, skip: int, limit: int) -> list[Project]:

        if limit - skip > 50:
            raise exceptions.TooBigRequest()

        q = select(self.model).limit(limit).offset(skip).order_by(
            desc(self.model.id)
        )
        projects = await self.db.execute(q)

        res = projects.scalars().unique().all()
        return res

    async def get_detail(self, id: int) -> Project:

        if not await self.object_is_exist(id=id):
            raise exceptions.ObjectDoesNotExist()

        q = select(self.model).where(self.model.id == id).join(
            self.model.tasks, isouter=True).options(joinedload(self.model.tasks))

        project = await self.db.execute(q)
        result = project.scalar()

        return result
