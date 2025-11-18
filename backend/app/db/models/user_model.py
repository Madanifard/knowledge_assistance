from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Mapped
from ..sql_db import Base


class User(Base):
    __tablename__ == "users"

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

    def __repr__(self) -> self:
        return f"<User {self.username}>"
