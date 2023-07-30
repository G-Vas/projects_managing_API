from .base import SQLAlchemyRepository
from models.models import User
import core.exceptions as exceptions
from sqlalchemy import select


class UserRepository(SQLAlchemyRepository):
    model: User = User

    async def get_by_email(self, email: str) -> User:

        q = select(self.model).where(self.model.email == email)
        user = await self.db.execute(q)
        if user is None:
            raise exceptions.ObjectDoesNotExist(f'user with email:{email} not found')
        return user.scalar_one()
