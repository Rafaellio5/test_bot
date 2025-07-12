from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from config.settings import BOT_TOKEN, BRANCHES

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Главное меню с филиалами
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(*[KeyboardButton(branch) for branch in BRANCHES])

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(
        "👋 Этот бот создан для корректной коммуникации с HelpDesk специалистами.\n"
        "Выберите филиал:", reply_markup=main_menu)

@dp.message_handler(lambda msg: msg.text in BRANCHES)
async def branch_selected(message: types.Message):
    branch = message.text
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for name, _ in BRANCHES[branch]:
        kb.add(KeyboardButton(name))
    kb.add(KeyboardButton("Выбор филиала"))
    await message.answer(f"📍 Вы выбрали: {branch}. Выберите специалиста:", reply_markup=kb)

@dp.message_handler(lambda msg: msg.text == "Выбор филиала")
async def back_to_menu(message: types.Message):
    await message.answer("🔁 Вернулись к списку филиалов. Выберите филиал:", reply_markup=main_menu)

@dp.message_handler()
async def specialist_selected(message: types.Message):
    for branch in BRANCHES.values():
        for name, link in branch:
            if message.text == name:
                await message.answer(f"👤 Связаться с {name}: {link}")
                return
