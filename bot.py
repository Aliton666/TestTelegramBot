from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from aiogram.types import *

from core.button import registration_markup, services_markup
from core.inline import procedure_inline, specialist_inline, time_menu, date_inline, time_inline
from database.dbusers import registration_users, check_users, get_procedures, get_specialists, create_appointment
from core.config import *
from database.dbusers import create_tables

create_tables()


import os
os.system("clear")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Временное хранилище для незавершенных записей
appointments = {}

@dp.message_handler(commands=["start"])
async def start(message: Message):
    user_id = message.chat.id
    check = check_users(user_id)
    
    if check is None:
        await message.reply("Вы не зарегистрированы. Пожалуйста, зарегистрируйтесь.", reply_markup=registration_markup)
    else:
        await message.reply("Вы уже у нас зарегистрированы, пользуйтесь на здоровье 😇", reply_markup=services_markup)

@dp.message_handler(content_types=ContentTypes.CONTACT)
async def add_contact(message: Message):
    user_id = message.contact.user_id
    username = message.chat.username
    first_name = message.contact.first_name
    last_name = message.contact.last_name
    phone = message.contact.phone_number
    registration_users(user_id, username, first_name, last_name, phone)

    appointments[user_id] = appointments.get(user_id, {})
    appointments[user_id]["phone"] = phone

    information = f"Айди: {user_id}\nПол(кое) Имя: @{username}\nИмя: {first_name}\nФамилия: {last_name}\nНомер: {phone}\nВремя записи: {datetime.now().strftime('%Y-%m-%d')}"
    await bot.send_message(chat_id=ADMIN_USERID, text=information)
    await message.reply(text="Вы были зарегистрированы в нашем сервисе, пользуйтесь на здоровье 😇", reply_markup=services_markup)

@dp.message_handler(content_types=ContentTypes.TEXT)
async def message_text_user(message: Message):
    user_id = message.chat.id
    check = check_users(user_id)
    if check is None:
        await message.answer("Пройдите регестрацию")
    else:
        if message.text.lower() == "услуги":
            await message.answer("Вы в Услуги", reply_markup=procedure_inline)
            await message.delete()

@dp.callback_query_handler(lambda c: c.data.startswith("procedure_"))
async def procedure_handler(callback_query: CallbackQuery):
    procedure_id = int(callback_query.data[len("procedure_"):])  # Получаем ID процедуры
    user_id = callback_query.from_user.id

    # Сохраняем выбранную процедуру для пользователя
    appointments[user_id] = appointments.get(user_id, {})
    appointments[user_id]["procedure_id"] = procedure_id

    # Сохраняем ID сообщения, чтобы редактировать его позже
    msg = await bot.edit_message_text(
        f"Выберите специалиста на процедуру {procedure_id}:", 
        chat_id=user_id, 
        message_id=callback_query.message.message_id, 
        reply_markup=specialist_inline
    )
    appointments[user_id]["msg_id_procedure"] = msg.message_id  # Сохраняем ID сообщения для дальнейшего редактирования



@dp.callback_query_handler(lambda c: c.data.startswith("specialist_"))
async def date_handler(callback_query: CallbackQuery):
    specialist_id = int(callback_query.data[len("specialist_"):])
    user_id = callback_query.from_user.id

    # Сохраняем ID специалиста
    appointments[user_id] = appointments.get(user_id, {})
    appointments[user_id]["specialist_id"] = specialist_id

    # Редактируем сообщение, отображая выбор даты
    msg = await bot.edit_message_text(
        "Выберите дату:",
        chat_id=callback_query.from_user.id,
        message_id=appointments[callback_query.from_user.id]["msg_id_procedure"],
        reply_markup=date_inline
    )

    # Сохраняем ID редактируемого сообщения
    appointments[callback_query.from_user.id]["msg_id_date"] = msg.message_id


@dp.callback_query_handler(lambda c: c.data.startswith("date_"))
async def time_handler(callback_query: CallbackQuery):
    # Извлекаем выбранную дату из callback_data
    selected_date = callback_query.data[len("date_"):]

    # Сохраняем выбранную дату в appointments
    appointments[callback_query.from_user.id]["date"] = selected_date

    # Получаем инлайн кнопки для выбора времени
    time_buttons = time_menu  # Уже инлайн кнопки созданы

    # Редактируем сообщение, отображая выбор времени
    msg = await bot.edit_message_text(
        "Выберите время:", 
        chat_id=callback_query.from_user.id, 
        message_id=appointments[callback_query.from_user.id]["msg_id_date"], 
        reply_markup=time_buttons
    )
    
    # Сохраняем ID редактируемого сообщения
    appointments[callback_query.from_user.id]["msg_id_date"] = msg.message_id

@dp.callback_query_handler(lambda c: c.data in ["10:00", "12:00", "14:00", "16:00"])
async def time_callback_handler(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    appointments[user_id]["time"] = callback_query.data
    await callback_query.answer(f"Вы выбрали время: {callback_query.data}")

    # Подтверждение записи
    appointment_details = appointments.get(user_id)
    if not appointment_details:
        await callback_query.message.answer("Не удалось найти данные о записи.")
        return

    await callback_query.message.answer("Подтвердите запись:\n\n"
                                        f"Телефон: {appointments[user_id]['phone']}\n"
                                        f"Процедура: {appointments[user_id]['procedure']}\n"
                                        f"Специалист: {appointments[user_id]['specialist']}\n"
                                        f"Дата: {appointments[user_id]['date']}\n"
                                        f"Время: {appointments[user_id]['time']}\n\n"
                                        "Если все верно, отправьте подтверждение.")

    # Создание записи в базе данных
    create_appointment(
        user_id, 
        appointments[user_id]["procedure_id"], 
        appointments[user_id]["specialist_id"], 
        appointments[user_id]["date"], 
        appointments[user_id]["time"]
    )

    # Отправка данных админу
    admin_message = (f"Новая запись:\n\n"
                     f"Телефон: {appointments[user_id]['phone']}\n"
                     f"Процедура: {appointments[user_id]['procedure']}\n"
                     f"Специалист: {appointments[user_id]['specialist']}\n"
                     f"Дата: {appointments[user_id]['date']}\n"
                     f"Время: {appointments[user_id]['time']}")
    await bot.send_message(ADMIN_USERID, admin_message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
