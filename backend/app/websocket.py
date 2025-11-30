from datetime import datetime
from typing import Dict
from fastapi.websockets import WebSocket


class WebSocketManager:
    def __init__(self):
        # task_id → WebSocket
        self.connections: Dict[str, WebSocket] = {}

    async def connect(self, task_id: str, websocket: WebSocket):
        await websocket.accept()
        self.connections[task_id] = websocket
        print(f"WebSocket connected for task: {task_id}")

    def disconnect(self, task_id: str):
        if task_id in self.connections:
            del self.connections[task_id]
            print(f"WebSocket disconnected: {task_id}")

    async def send_message(self, task_id: str, message: dict):
        if websocket := self.connections.get(task_id):
            try:
                await websocket.send_json(message)
            except:
                # اگر کلاینت قطع شده بود، پاکش کن
                self.disconnect(task_id)

    async def broadcast_progress(self, task_id: str, progress: int):
        await self.send_message(task_id, {
            "type": "progress",
            "task_id": task_id,
            "progress": progress
        })

    async def send_completed(self, task_id: str, result: dict, message: str = ""):
        await self.send_message(task_id, {
            "type": "completed",
            "task_id": task_id,
            "message": message,
            "result": result,
            "finished_at": datetime.now().isoformat()
        })

    async def send_error(self, task_id: str, error: str):
        await self.send_message(task_id, {
            "type": "error",
            "task_id": task_id,
            "error": error
        })
