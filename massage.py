import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- КНОПКИ ---

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="📅 Записаться"), types.KeyboardButton(text="💆‍♂️ Подобрать массаж")],
        [types.KeyboardButton(text="🎁 Акции"), types.KeyboardButton(text="📍 Адрес")]
    ],
    resize_keyboard=True
)

# --- СТАРТ ---

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! 👋\n\nЯ помогу подобрать массаж и записать тебя на удобное время.\n\nЧто хочешь сделать?",
        reply_markup=main_kb
    )

# --- ЗАПИСЬ ---

@dp.message(lambda message: message.text == "📅 Записаться")
async def booking(message: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Расслабляющий"), types.KeyboardButton(text="Лечебный")],
            [types.KeyboardButton(text="Антицеллюлитный"), types.KeyboardButton(text="Спортивный")]
        ],
        resize_keyboard=True
    )
    await message.answer("Выбери тип массажа 👇", reply_markup=kb)

# --- ЗАПУСК ---

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
