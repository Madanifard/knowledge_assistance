from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv()

# برای PostgreSQL (توصیه شده در تولید)
# DATABASE_URL = os.getenv(
#     "DATABASE_URL",
#     "postgresql+asyncpg://user:password@localhost/dbname"  # تغییر بده
# )

# برای تست سریع با SQLite
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=False)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False)


# Base برای تمام مدل‌ها
class Base(DeclarativeBase):
    pass


# تابع برای استفاده در dependency
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
