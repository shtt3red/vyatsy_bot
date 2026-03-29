import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

from ai_api import get_recommendation

TELEGRAM_TOKEN = "8538443655:AAGuOVqxW5Ln0iYVaWZ4cSNb1DnCPVQRcV8"
ADMIN_USERNAME = "@axy3nno"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

user_mode = {}

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="подобрать сообщество")],
        [KeyboardButton(text="администрация")]
    ],
    resize_keyboard=True
)


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("выбери действие:", reply_markup=keyboard)


@dp.message(lambda m: m.text == "подобрать сообщество")
async def ai_mode(message: types.Message):
    user_mode[message.from_user.id] = True
    await message.answer("напиши интерес (минимум 3 слова)")


@dp.message(lambda m: m.text == "администрация")
async def admin(message: types.Message):
    await message.answer(f"связь: {ADMIN_USERNAME}")


@dp.message()
async def handle(message: types.Message):
    if not user_mode.get(message.from_user.id):
        return

    text = message.text.strip()

    if len(text.split()) < 3:
        await message.answer(
            "⚠️ напиши интерес подробнее\n\n"
            "Пример:\n"
            "• хочу снимать видео и монтировать\n"
            "• интересуюсь наукой и исследованиями\n"
            "• люблю спорт и соревнования"
        )
        return

    result = get_recommendation(text)

    await message.answer(
    f"✨ Подбор для тебя:\n\n{result}\n\n"
    "💬 Можешь написать другой интерес"
)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
