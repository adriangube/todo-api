from sqlalchemy import String, Boolean, Integer
from .database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[str] = mapped_column(String, default="user")


class Todos(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String, nullable=True)
    complete: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
