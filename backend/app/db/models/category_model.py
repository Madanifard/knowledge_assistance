from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship
from app.db.sql_db import Base

if TYPE_CHECKING:
    from app.db.models.document_model import Document
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = Column(
        Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(
        String(100), unique=True, index=True, nullable=False)

    files: Mapped[list["Document"]] = relationship(
        "Document",
        back_populates="category",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Category {self.name}>"