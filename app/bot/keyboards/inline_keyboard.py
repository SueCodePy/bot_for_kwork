from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_pars_keyboard():

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Запустить парсер', callback_data='pars_data')]])
    return keyboard

def next_kwork_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='Показать следующий кворк', callback_data='next_data')]])
    return keyboard

def show_first_kwork_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='Показать первый кворк из списка', callback_data='view_data')]])
    return keyboard

