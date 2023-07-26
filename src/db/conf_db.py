from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from core.conf import DATABASE_URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base


engine = create_async_engine(DATABASE_URL, echo=True)

Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Dependency
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
