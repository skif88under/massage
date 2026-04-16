import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ---------------- КНОПКИ ----------------

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📅 Записаться"), KeyboardButton(text="💆‍♂️ Подобрать массаж")],
        [KeyboardButton(text="🎁 Акции"), KeyboardButton(text="📍 Адрес")]
    ],
    resize_keyboard=True
)

massage_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Расслабляющий"), KeyboardButton(text="Лечебный")],
        [KeyboardButton(text="Антицеллюлитный"), KeyboardButton(text="Спортивный")]
    ],
    resize_keyboard=True
)

time_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="60 минут"), KeyboardButton(text="90 минут")]
    ],
    resize_keyboard=True
)

slot_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сегодня вечер"), KeyboardButton(text="Завтра утро")],
        [KeyboardButton(text="Завтра день"), KeyboardButton(text="Другое время")]
    ],
    resize_keyboard=True
)

contact_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 Отправить контакт", request_contact=True)]
    ],
    resize_keyboard=True
)

# ---------------- START ----------------

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет! 👋\n\nЯ помогу подобрать массаж и записаться на удобное время.",
        reply_markup=main_kb
    )

# ---------------- ЗАПИСЬ ----------------

@dp.message(F.text == "📅 Записаться")
async def book(message: Message):
    await message.answer("Выбери тип массажа 👇", reply_markup=massage_kb)

@dp.message(F.text.in_({"Расслабляющий", "Лечебный", "Антицеллюлитный", "Спортивный"}))
async def choose_duration(message: Message):
    await message.answer("Сколько по времени?", reply_markup=time_kb)

@dp.message(F.text.in_({"60 минут", "90 минут"}))
async def choose_time(message: Message):
    await message.answer("Выбери удобное время 👇", reply_markup=slot_kb)

@dp.message(F.text.in_({"Сегодня вечер", "Завтра утро", "Завтра день", "Другое время"}))
async def get_contact(message: Message):
    await message.answer("Оставь номер телефона 👇", reply_markup=contact_kb)

@dp.message(F.contact)
async def contact_received(message: Message):
    phone = message.contact.phone_number

    await bot.send_message(
        ADMIN_ID,
        f"💆‍♂️ Новая запись!\nТелефон: {phone}"
    )

    await message.answer(
        "Готово 🙌 Ты записан! Я скоро свяжусь с тобой.",
        reply_markup=main_kb
    )

# ---------------- КВИЗ ----------------

@dp.message(F.text == "💆‍♂️ Подобрать массаж")
async def quiz(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Спина / шея"), KeyboardButton(text="Стресс / усталость")],
            [KeyboardButton(text="Отёки / тело"), KeyboardButton(text="После спорта")]
        ],
        resize_keyboard=True
    )

    await message.answer("Что сейчас беспокоит больше всего?", reply_markup=kb)

@dp.message(F.text.in_({"Спина / шея", "Стресс / усталость", "Отёки / тело", "После спорта"}))
async def result(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 Записаться")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "Тебе подойдёт массаж с проработкой проблемных зон 💆‍♂️\n\n"
        "🎁 Сейчас есть скидка на первый сеанс",
        reply_markup=kb
    )

# ---------------- ПРОЧЕЕ ----------------

@dp.message(F.text == "🎁 Акции")
async def promo(message: Message):
    await message.answer(
        "🎁 Скидка на первый сеанс\n🎁 Бонус при курсе 3–5 сеансов\n\n"
        "Хочешь записаться?"
    )

@dp.message(F.text == "📍 Адрес")
async def address(message: Message):
    await message.answer("📍 Напиши сюда свой адрес кабинета")

# ---------------- RUN ----------------

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
