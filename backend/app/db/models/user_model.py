from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Mapped, relationship
from app.db.sql_db import Base

if TYPE_CHECKING:
    from app.db.models.document_model import Document

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(
        Integer, primary_key=True, index=True)
    username: Mapped[str] = Column(
        String(50), unique=True, index=True, nullable=False)
    email: Mapped[str | None] = Column(
        String(255), unique=True, index=True, nullable=True)
    hashed_password: Mapped[str] = Column(
        String(255), unique=True, index=True, nullable=False)
    is_active: Mapped[bool] = Column(
        Boolean, default=True)

    files: Mapped[list["Document"]] = relationship(
        "Document",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<User {self.username}>"

    