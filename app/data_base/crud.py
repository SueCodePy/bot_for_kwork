from app.data_base.models import Kwork, User, UserKwork
from app.data_base.connection import get_session
from sqlalchemy import select, func, update
from sqlalchemy.dialects.postgresql import insert
import asyncio


async def add_kwork(kw_id, descr, kw_cnt, kw_price, url_page):
    async with get_session() as session:
        result = await session.execute(select(Kwork).where(Kwork.id == kw_id))
        kwork = result.scalar_one_or_none()
        if not kwork:
            new_kwork = Kwork(id=kw_id, description=descr, kwork_count=kw_cnt, price=kw_price, url=url_page)
            session.add(new_kwork)
            await session.commit()
            return True



async def update_kwork_viewed_for_user(kw_id, user_id):

    """Функция обновляет состояние кворка для пользователя. По умолчанию пользователь не видевший кворк, атрибут viewed = False. Если же пользователь просмотрел кворк viewed = True"""

    async with get_session() as session:
        result = await session.execute(select(UserKwork).where(UserKwork.kwork_id == kw_id, UserKwork.user_id == user_id))
        kwork = result.scalar_one_or_none()
        if kwork:
            kwork.viewed = True  # после просмотра кворка, меняется статус
            await session.commit()


async def add_user_in_waiting(user_id):
    """Функция добавит пользователя в очередь на просмотры новых кворков"""
    async with get_session() as session:
        user = await session.get(User, user_id)
        if user:
            user.viewed_all = True
            await session.commit()


async def get_users_in_waiting()->list[int]:
    """Функция вернет список пользователей ожидающие кворки. Пользователи, которые просмотрели все кворки и ожидают еще атрибут User.viewed_all == True"""
    async with get_session() as session:
        result = await session.execute(select(User.telegram_id).where(User.viewed_all == True))
        users = result.scalars().all()

        return users


async def add_user(user_id):
    """Функция добавит пользователя в тадлицу users"""

    async with get_session() as session:
        user = await session.get(User, user_id)
        if not user:
            user = User(telegram_id=user_id)
            session.add(user)
            await session.commit()


async def delete_user_in_waiting(user_id):
    """Функция меняет состояние ожидания в таблице user через атрибут user.viewed_all по умолчанию False если есть не просмотренные кворки, пользователь в состоянии чтения в таблице users"""

    async with get_session() as session:
        user = await session.get(User, user_id)
        if user and user.viewed_all:
            user.viewed_all = False
            await session.commit()


async def show_kwork(user_id):
    """Функция возвращает первый найденный кворк для пользователя"""
    async with get_session() as session:
        result = await session.execute(select(Kwork).join(UserKwork).where(UserKwork.viewed == False, UserKwork.user_id == user_id).limit(1))
        kwork = result.scalars().first() # берёт первый объект или None, если нет

        return kwork


async def get_all_users():
    async with get_session() as session:
        users = await session.execute(select(User.telegram_id))
        return users.scalars().all()



async def assign_kworks_to_user(user_id: int, kworks: list[int] | None = None) -> None:
    """Привязывает кворки к пользователю. Дубликаты игнорируются."""

    async with get_session() as session:
        # Если список кворков не передан — берём все кворки из базы
        if kworks is None:
            result = await session.execute(select(Kwork.id))
            kworks = result.scalars().all()

        # Формируем bulk insert с on_conflict_do_nothing
        stmt = insert(UserKwork).values([
            {"user_id": user_id, "kwork_id": kw_id}
            for kw_id in kworks
        ]).on_conflict_do_nothing(
            index_elements=["user_id", "kwork_id"]  # ключ уникальности
        )

        await session.execute(stmt)
        await session.commit()



async def delete_kwork():
    pass                  # не знаю еще как проработать удаление кворков, на сайте пометка актив но когда кворк изчезает просрочивается то наврядли они хранятся в базе сайта. в общем пока не срочно, подумаю потом, может заведу еще столбец с датой и раз в неделю завопускать автоматом функцию которая будет удалять те кворки которым больше недели.
    """ Функция проходит по кворкам в таблице kwork, """


if __name__ == '__main__':
    async def main():
        kwork = await show_kwork(247382919)  # твой user_id

        print(await get_users_in_waiting())
        print(f"Пользователь {247382919}, кворк: {kwork}")
        if kwork:
            print(kwork.id, kwork.description)
        else:
            print("Нет непросмотренных кворков")

    asyncio.run(main())