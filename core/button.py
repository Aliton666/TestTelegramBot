from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


registration_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(text="Зарегистрироваться", request_contact=True)
)

services_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(text="Услуги")
)