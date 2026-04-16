import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- КНОПКИ ---

main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add("📅 Записаться", "💆‍♂️ Подобрать массаж")
main_kb.add("🎁 Акции", "📍 Адрес")

massage_kb = ReplyKeyboardMarkup(resize_keyboard=True)
massage_kb.add("Расслабляющий", "Лечебный")
massage_kb.add("Антицеллюлитный", "Спортивный")

time_kb = ReplyKeyboardMarkup(resize_keyboard=True)
time_kb.add("Сегодня вечер", "Завтра утро")
time_kb.add("Завтра день", "Другое время")

quiz1_kb = ReplyKeyboardMarkup(resize_keyboard=True)
quiz1_kb.add("Спина / шея", "Стресс / усталость")
quiz1_kb.add("Отёки / тело", "После спорта")

quiz2_kb = ReplyKeyboardMarkup(resize_keyboard=True)
quiz2_kb.add("Убрать боль", "Расслабиться")
quiz2_kb.add("Подтянуть тело", "Восстановиться")

yes_kb = ReplyKeyboardMarkup(resize_keyboard=True)
yes_kb.add("📅 Записаться", "Задать вопрос")

# --- СТАРТ ---

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "Привет! 👋\n\nЯ помогу подобрать массаж и записать тебя на удобное время.\n\nЧто хочешь сделать?",
        reply_markup=main_kb
    )

# --- ЗАПИСЬ ---

@dp.message_handler(lambda message: message.text == "📅 Записаться")
async def booking(message: types.Message):
    await message.answer("Выбери тип массажа 👇", reply_markup=massage_kb)

@dp.message_handler(lambda message: message.text in ["Расслабляющий", "Лечебный", "Антицеллюлитный", "Спортивный"])
async def choose_time(message: types.Message):
    await message.answer("Сколько по времени?", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add("60 минут", "90 минут"))

@dp.message_handler(lambda message: message.text in ["60 минут", "90 минут"])
async def choose_slot(message: types.Message):
    await message.answer("Выбери удобное время 👇", reply_markup=time_kb)

@dp.message_handler(lambda message: message.text in ["Сегодня вечер", "Завтра утро", "Завтра день", "Другое время"])
async def contact(message: types.Message):
    contact_btn = ReplyKeyboardMarkup(resize_keyboard=True)
    contact_btn.add(KeyboardButton("Отправить контакт", request_contact=True))
    await message.answer("Оставь номер телефона 👇", reply_markup=contact_btn)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_contact(message: types.Message):
    phone = message.contact.phone_number

    # сюда вставь свой ID
    ADMIN_ID = 5261204876

    await bot.send_message(ADMIN_ID, f"Новая заявка!\nТелефон: {phone}")

    await message.answer(
        "Готово 🙌\n\nТы записан! Я скоро свяжусь с тобой.",
        reply_markup=main_kb
    )

# --- КВИЗ ---

@dp.message_handler(lambda message: message.text == "💆‍♂️ Подобрать массаж")
async def quiz1(message: types.Message):
    await message.answer("Что сейчас беспокоит больше всего?", reply_markup=quiz1_kb)

@dp.message_handler(lambda message: message.text in ["Спина / шея", "Стресс / усталость", "Отёки / тело", "После спорта"])
async def quiz2(message: types.Message):
    await message.answer("Какой результат хочешь?", reply_markup=quiz2_kb)

@dp.message_handler(lambda message: message.text in ["Убрать боль", "Расслабиться", "Подтянуть тело", "Восстановиться"])
async def result(message: types.Message):
    await message.answer(
        "Тебе подойдёт массаж с проработкой проблемных зон + расслабление 💆‍♂️\n\n"
        "🎁 Сейчас есть скидка на первый сеанс\n\nХочешь записаться?",
        reply_markup=yes_kb
    )

# --- АКЦИИ ---

@dp.message_handler(lambda message: message.text == "🎁 Акции")
async def promo(message: types.Message):
    await message.answer(
        "🎁 Скидка на первый сеанс\n🎁 Бонус при записи курса\n\nХочешь записаться?",
        reply_markup=yes_kb
    )

# --- АДРЕС ---

@dp.message_handler(lambda message: message.text == "📍 Адрес")
async def address(message: types.Message):
    await message.answer("Я нахожусь здесь: (вставь адрес)")

# --- ЗАПУСК ---

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
