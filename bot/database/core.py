from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine

from config import settings


engine = create_async_engine(settings.DB_URL)
session_factory = async_sessionmaker(engine)


class Base(DeclarativeBase):
    pass


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
