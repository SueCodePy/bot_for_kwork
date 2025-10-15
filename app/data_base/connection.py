
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from config.config import settings


url_db =  (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}"
          f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")


engine = create_async_engine(url_db, echo=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def get_session()->AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session