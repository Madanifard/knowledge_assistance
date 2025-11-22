from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped
from app.db.sql_db import Base

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = Column(
        Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(
        String(100), unique=True, index=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Category {self.name}>"