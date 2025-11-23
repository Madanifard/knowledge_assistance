from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv
from typing import AsyncGenerator

load_dotenv()

# برای PostgreSQL (توصیه شده در تولید)
DATABASE_URL = os.getenv(
    "SQL_DATABASE_URL",
    "sqlite+aiosqlite:///./fastapi_jwt.db")


engine = create_async_engine(DATABASE_URL, echo=False)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False)


# Base برای تمام مدل‌ها
class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
