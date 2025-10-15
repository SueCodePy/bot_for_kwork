import asyncio
import logging
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest

from app.bot.keyboards.inline_keyboard import  show_first_kwork_keyboard
from app.data_base.crud import get_all_users, assign_kworks_to_user
from app.parsing.parser_kwork import run_parser
from app.data_base.crud import get_users_in_waiting, delete_user_in_waiting
from app.bot.bot import bot


logging.basicConfig(level=logging.INFO)

async def notifier():
    while True:
        try:
            kwork_id = await run_parser()
            logging.info(f"[notifier] run_parser вернул: {len(kwork_id)}")

            if kwork_id and len(kwork_id) > 0:
                users_waiting = await get_users_in_waiting()
                all_user = await get_all_users()
                logging.info(f"[notifier] найдено {len(users_waiting)} пользователей в ожидании")


                for user in all_user:
                    if user:
                        await assign_kworks_to_user(user, kwork_id)

                        if users_waiting and user in users_waiting:

                            try:
                                logging.info(f"[notifier] отправляю сообщение пользователю {user}")
                                await bot.send_message(
                                        chat_id=user,
                                        text=f'Собрано {len(kwork_id)}',
                                        reply_markup=show_first_kwork_keyboard()  )
                                await delete_user_in_waiting(user)
                                logging.info(f"[notifier] пользователь {user} удалён из ожидания")
                            except TelegramForbiddenError:            # если пользователь заблокировал бота
                                logging.warning(f"[notifier] пользователь {user} заблокировал бота")
                                await delete_user_in_waiting(user)
                            except TelegramBadRequest as e:          # если проблема со стороны интернета
                                logging.error(f"[notifier] TelegramBadRequest для {user}: {e}")

        except asyncio.CancelledError:

            logging.info("[notifier] задача была отменена")
            raise  # обязательно пробрасываем, чтобы on_shutdown отработал правильно


        except Exception as e:
            logging.error(f"[notifier] глобальная ошибка: {e}")

        await asyncio.sleep(120)  # уменьшил для отладки