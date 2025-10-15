import asyncio
import logging

from app.bot.bot import dp, bot
from app.bot.handlers.handlers import router
from app.data_base.connection import engine
from app.data_base.models import Base
from app.parsing.notifier import notifier


notifier_task: asyncio.Task | None = None   # Фоновая задача уведомлений


async def on_startup():
    """Действия при старте бота"""
    global notifier_task
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Запуск фоновой задачи
    notifier_task = asyncio.create_task(notifier())



async def on_shutdown():
    """Закрытие ресурсов при остановке бота"""
    global notifier_task

    if notifier_task and not notifier_task.done():
        notifier_task.cancel()
        try:
            await notifier_task
        except asyncio.CancelledError:
            logging.info("Фоновая задача notifier остановлена")

    await engine.dispose()
    logging.info("Подключение к базе закрыто")


async def main():
    dp.include_router(router)

    # Регистрируем хуки
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

