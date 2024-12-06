from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta

# Список процедур

procedure_inline = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text="Процедура1", callback_data="procedure_1"),
    InlineKeyboardButton(text="Процедура2", callback_data="procedure_2"),
    InlineKeyboardButton(text="Процедура3", callback_data="procedure_3")
)


specialist_inline = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text="Специалист1", callback_data="specialist_1"),
    InlineKeyboardButton(text="Специалист2", callback_data="specialist_2"),
    InlineKeyboardButton(text="Специалист3", callback_data="specialist_3"),
)


# Кнопки для выбора времени
time_inline = [
    InlineKeyboardButton("10:00", callback_data="10:00"),
    InlineKeyboardButton("12:00", callback_data="12:00"),
    InlineKeyboardButton("14:00", callback_data="14:00"),
    InlineKeyboardButton("16:00", callback_data="16:00")
]
time_menu = InlineKeyboardMarkup(row_width=2)
time_menu.add(*time_inline)

#  Функция для генерации списка доступных дат (например, на неделю вперед)
def generate_dates():
    today = datetime.today()
    dates = [(today + timedelta(days=i)).strftime("%d-%m-%Y") for i in range(7)]  # Генерация 7 дней вперед
    return dates

# Генерация инлайн кнопок для каждой даты
def generate_date_buttons(dates):
    buttons = [InlineKeyboardButton(date, callback_data=f"date_{date}") for date in dates]
    return InlineKeyboardMarkup(row_width=2).add(*buttons)  # Вы можете настроить row_width

# Генерация доступных дат
dates = generate_dates()

# Генерация инлайн клавиатуры для дат
date_inline = generate_date_buttons(dates)