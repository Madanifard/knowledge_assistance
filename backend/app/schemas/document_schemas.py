from pydantic import BaseModel
from datetime import datetime

class DocumentOut(BaseModel):
    id: int
    user_id: int
    category_id: int
    name: str
    file_path: str
    file_type: str
    file_size: int
    created_at: datetime

    class Config:
        from_attributes = True  # برای SQLAlchemy 2.0
