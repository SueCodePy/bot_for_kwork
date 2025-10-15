from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    viewing = State()  # пользователь листает кворки
    waiting = State()  # ждет новых