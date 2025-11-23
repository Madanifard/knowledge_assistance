# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.sql_db import engine, Base
from app.routers import auth, users, category


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---------- Startup ----------
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # ساخت جداول
    print("Database connected & tables created (if not exists)")

    # می‌تونی اینجا چیزای دیگه هم راه‌اندازی کنی:
    # - Redis connection
    # - Cache warmup
    # - Background scheduler
    # - Logging setup
    yield

    # ---------- Shutdown ----------
    await engine.dispose()  # خیلی مهمه! اتصالات async رو تمیز می‌کنه
    print("Database connection closed")


app = FastAPI(
    title="FastAPI JWT + SQLAlchemy 2.0",
    description="احراز هویت حرفه‌ای — کاملاً مدرن با lifespan",
    version="1.0.0",
    lifespan=lifespan,  # اینجا استفاده می‌شه
)

# روترها
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(category.router)


@app.get("/")
async def root():
    return {"message": "سلام! API آماده است — مستندات: /docs"}
