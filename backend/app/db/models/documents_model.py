from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from app.db.sql_db import Base
from app.db.models.user_model import User
from app.db.models.category_model import Category


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = Column(
        Integer, primary_key=True, index=True)
    user_id: Mapped[int] = Column(
        Integer, ForeignKey("users.id"), index=True, nullable=False)
    user: Mapped["User"] = relationship(
        "User", back_populates="files")
    category_id: Mapped[int] = Column(
        Integer, ForeignKey("categories.id"), index=True, nullable=False)
    category: Mapped["Category"] = relationship(
        "Category", back_populates="files")
    name: Mapped[str] = Column(
        String(255), unique=True, index=True, nullable=False)
    filepath: Mapped[str] = Column(
        String(500), unique=True, index=True, nullable=True)

    def __repr__(self) -> str:
        return f"<File {self.name}>"
