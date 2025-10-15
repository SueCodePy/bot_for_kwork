import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from ..fsm.states import UserStates
from ..keyboards.inline_keyboard import next_kwork_keyboard, show_first_kwork_keyboard
from app.parsing.parser_kwork import run_parser
from app.data_base.crud import show_kwork, update_kwork_viewed_for_user, add_user, assign_kworks_to_user, \
    add_user_in_waiting

from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter


router = Router()


@router.message(F.text == "/start")
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await add_user(user_id)
    await assign_kworks_to_user(user_id)
    await message.answer('Парсер в работе! Удачи в поиске выгодного кворка! ', reply_markup=show_first_kwork_keyboard())
    await state.set_state(UserStates.waiting)
    await add_user_in_waiting(user_id)


@router.callback_query(F.data == 'view_data', StateFilter(UserStates.waiting))
async def viewing_data(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    kwork = await show_kwork(user_id)

    if kwork:

        await call.message.answer(f'{kwork.description}\n{kwork.kwork_count}\n{kwork.price}\n{kwork.url}', reply_markup=next_kwork_keyboard())
        await update_kwork_viewed_for_user(kwork.id, user_id)
        await state.set_state(UserStates.viewing)

    else:
        await call.message.answer(f'Свежих кворков пока нет😏. Дам знать, как появится.')
        await add_user_in_waiting(user_id)




@router.callback_query(F.data == 'next_data', StateFilter(UserStates.viewing))
async def show_new_kwork(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    kwork = await show_kwork(user_id)
    if kwork:
        await call.message.answer(f'{kwork.description}\n{kwork.kwork_count}\n{kwork.price}\n{kwork.url}', reply_markup=next_kwork_keyboard())
        await update_kwork_viewed_for_user(kwork.id, user_id)
        await state.set_state(UserStates.viewing)
    else:
        await call.message.answer('Свежих кворков пока нет😏. Дам знать, как появится.')
        await state.set_state(UserStates.waiting)
        await add_user_in_waiting(user_id)
