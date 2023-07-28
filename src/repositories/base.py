from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, func, delete
import core.exceptions as exceptions


class IRepository(ABC):

    @abstractmethod
    async def add(self):
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: int):
        raise NotImplementedError

    @abstractmethod
    async def delete(id: int):
        raise NotImplementedError


class SQLAlchemyRepository(IRepository):

    model: None

    def __init__(self, db: AsyncSession) -> None:
        self.db: AsyncSession = db

    async def add(self, data: dict):

        q = insert(self.model).values(**data).returning(self.model)
        res = await self.db.execute(q)
        await self.db.commit()
        return res.scalar_one()

    async def get(self, id: int):

        if not await self.object_is_exist(id=id):
            raise exceptions.ObjectDoesNotExist()

        q = select(self.model).where(self.model.id == id)
        task = await self.db.execute(q)
        return task.scalar_one()

    async def delete(self, id: int) -> dict:

        if not await self.object_is_exist(id=id):
            raise exceptions.ObjectDoesNotExist()

        await self.db.execute(delete(self.model).where(self.model.id == id))
        await self.db.commit()
        return {'ok': True}

    async def object_is_exist(self, id: int) -> bool:

        objects_count = await self.db.execute(
            select(func.count("id")).select_from(self.model).where(self.model.id == id)
        )
        if objects_count.scalar() < 1:
            return False
        return True
