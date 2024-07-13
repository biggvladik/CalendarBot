from sqlalchemy import DateTime, Float, String, Text, func,BOOLEAN
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_ext: Mapped[str] = mapped_column(String(150), nullable=False)



class User(Base):
    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    is_admin: Mapped[bool] = mapped_column(BOOLEAN)

class Message(Base):
    __tablename__ = 'messages'

    date_str: Mapped[str] = mapped_column(String(150), nullable=False)
    message_str: Mapped[str] = mapped_column(String(500), nullable=False)
    approve: Mapped[bool] = mapped_column(BOOLEAN)
