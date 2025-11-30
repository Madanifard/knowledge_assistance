# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocketDisconnect, WebSocket
from websocket import WebSocketManager

from app.db.sql_db import engine, Base

from app.db.models.user_model import User
from app.db.models.category_model import Category
from app.db.models.document_model import Document

from app.routers import auth, users, documents
from app.routers import categories


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
app.include_router(categories.router)
app.include_router(documents.router)

websocket_manager = WebSocketManager()

# ──────────────────────────────
# WebSocket Endpoint
# ──────────────────────────────
@app.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    await websocket_manager.connect(task_id, websocket)
    try:
        # فقط keep-alive می‌کنیم تا اتصال باز بمونه
        while True:
            data = await websocket.receive_text()  # منتظر پیام از کلاینت (اختیاری)
            # می‌تونی اینجا دستورات دیگه مثل "cancel" بگیری
    except WebSocketDisconnect:
        websocket_manager.disconnect(task_id)
    except Exception as e:
        websocket_manager.disconnect(task_id)


@app.get("/")
async def root():
    return {"message": "سلام! API آماده است — مستندات: /docs"}
