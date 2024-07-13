from sqlalchemy import DateTime, Float, String, Text, func,BOOLEAN
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_ext: Mapped[str] = mapped_column(String(150), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    is_admin: Mapped[bool] = mapped_column(BOOLEAN)

class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_ext: Mapped[str] = mapped_column(String(150), nullable=False)

    date_str: Mapped[str] = mapped_column(String(150), nullable=False)
    message_str: Mapped[str] = mapped_column(String(500), nullable=False)
    approve: Mapped[bool] = mapped_column(BOOLEAN)
