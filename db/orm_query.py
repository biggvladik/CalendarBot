from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from .models import User, Message

from factory import make_str


async def select_user_name(session: AsyncSession, id_ext: str):
    query = select(User).where(User.id_ext == id_ext)
    result = await session.execute(query)
    res = result.fetchone()
    return (lambda x: True if x else False)(res)


async def select_all_users(session: AsyncSession):
    query = select(User.id_ext, User.name)
    result = await session.execute(query)
    return result.fetchall()


async def insert_user(session: AsyncSession, id_ext: int, name: str):
    user_flag_id_query = select(User.id).where(User.id_ext == id_ext)
    user_flag_id = await session.execute(user_flag_id_query)
    user_flag_name_query = select(User.id).where(User.name == name)
    user_flag_name = await session.execute(user_flag_name_query)

    if user_flag_id.fetchone() or user_flag_name.fetchone():
        return 'Имя/ID уже присутствует в БД!'
    user = User(
        id_ext=id_ext,
        name=name,
        is_admin=False,
    )

    session.add(user)
    await session.commit()
    return False


async def delete_user(session: AsyncSession, id_ext: int):
    query = delete(User).where(User.id_ext == id_ext)
    await session.execute(query)
    await session.commit()


async def select_all_users_new(session: AsyncSession):
    query = select(User.id_ext, User.name)
    result = await session.execute(query)

    return [{'id': i[0], 'name': i[1], 'event': []} for i in result.fetchall()]


async def insert_message_logs(session: AsyncSession, date_str: str, message: dict):
    message_flag_query = select(Message.id).where(Message.date_str == date_str,Message.message_str == make_str(message['event']))
    message_flag_id = await session.execute(message_flag_query)
    message_flag_id = (lambda x: True if x else False)(message_flag_id.fetchone())
    if not message_flag_id:
        message = Message(
            id_ext=message['id'],
            date_str=date_str,
            message_str=make_str(message['event']),
            approve=False,
        )
        session.add(message)
        await session.commit()


async def change_status_message(session: AsyncSession, date_str: str, id_ext: str):
    query = update(Message).where(Message.id_ext == id_ext, Message.date_str == date_str).values(
        approve=True
    )
    await session.execute(query)
    await session.commit()


async def check_admin_user(session: AsyncSession, id_ext: int):
    query = select(Message).where(Message.id_ext == id_ext)
    result = await session.execute(query)
    if result:
        return True
    return False


async def select_events_by_date(session: AsyncSession, date_str: str):
    query = select(Message.date_str, Message.id_ext, Message.approve, User.name) \
        .join(User, Message.id_ext == User.id_ext) \
        .filter(Message.date_str == date_str)

    result = await session.execute(query)
    return result.fetchall()


async def select_user_name_by_id(session: AsyncSession, id_ext: str):
    query = select(User.name).where(User.id_ext == id_ext)
    result = await session.execute(query)
    res = result.fetchone()
    return (lambda x: x[0] if x else 'Пусто')(res)