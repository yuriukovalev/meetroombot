import os
import logging
import datetime
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from dotenv import load_dotenv
from data import DATA

# 🔹 1. Загружаем токены и настройки из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("🔴 BOT_TOKEN не найден! Проверь .env")

# 🔹 2. Настраиваем хранилище FSM
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

# 🔹 3. Файл логов 📂
LOG_FILE = "bot_usage.log"

def log_action(user_id, action):
    """ Записываем действия пользователя в файл логов """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} | User {user_id} | {action}\n"
    with open(LOG_FILE, "a") as file:
        file.write(log_entry)

# 🔹 4. Определяем состояния FSM
class BookingState(StatesGroup):
    choosing_city = State()
    choosing_office = State()
    choosing_floor = State()
    choosing_room = State()

# 📌 /start — Главное меню
@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(BookingState.choosing_city)

    log_action(message.from_user.id, "Вошел в бота (/start)")

    markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=city)] for city in DATA.keys()], resize_keyboard=True
    )

    print(f"🎯 Установлено состояние: {await state.get_state()}")  
    await message.answer("🏙 Выбери город:", reply_markup=markup)

# 📌 Выбор города
@dp.message(StateFilter(BookingState.choosing_city), F.text.in_(DATA.keys()))
async def choose_city(message: types.Message, state: FSMContext):
    city = message.text
    await state.update_data(city=city)
    await state.set_state(BookingState.choosing_office)

    log_action(message.from_user.id, f"Выбрал город: {city}")

    offices = DATA.get(city, {})
    if not offices:
        return await message.answer("❌ В этом городе нет доступных офисов.")

    markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=office)] for office in offices.keys()] + [[KeyboardButton(text="⬅️ Назад")]],
        resize_keyboard=True
    )

    await message.answer(f"🏙 Ты выбрал {city}. Теперь выбери офис:", reply_markup=markup)

# 📌 Выбор офиса
@dp.message(StateFilter(BookingState.choosing_office), F.text)
async def choose_office(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await start(message, state)
        return
    
    user_data = await state.get_data()
    city = user_data.get("city", "")

    office = message.text
    if office not in DATA.get(city, {}):
        return await message.answer("❌ Такого офиса нет! Выберите из списка.")

    await state.update_data(office=office)
    log_action(message.from_user.id, f"Выбрал офис: {office} (Город: {city})")

    # 🏢 Проверяем, нужны ли этажи
    office_data = DATA[city][office]
    if isinstance(office_data, dict) and all(isinstance(v, dict) for v in office_data.values()):
        await state.set_state(BookingState.choosing_floor)
        floors = office_data.keys()

        markup = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=floor)] for floor in floors] + [[KeyboardButton(text="⬅️ Назад")]],
            resize_keyboard=True
        )
        return await message.answer(f"🏢 Офис {office}. Выберите этаж:", reply_markup=markup)

    await state.set_state(BookingState.choosing_room)
    rooms = office_data
    if not rooms:
        return await message.answer("❌ В этом офисе нет переговорных.")

    markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=room)] for room in rooms.keys()] + [[KeyboardButton(text="⬅️ Назад")]],
        resize_keyboard=True
    )

    await message.answer(f"🏢 Ты выбрал {office}. Теперь выбери переговорную:", reply_markup=markup)

# 📌 Выбор этажа
@dp.message(StateFilter(BookingState.choosing_floor))
async def choose_floor(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await choose_office(message, state)
        return

    user_data = await state.get_data()
    city, office = user_data.get("city"), user_data.get("office")

    floor = message.text
    if floor not in DATA.get(city, {}).get(office, {}):
        return await message.answer("❌ Такого этажа нет! Выберите из списка.")

    await state.update_data(floor=floor)
    await state.set_state(BookingState.choosing_room)

    log_action(message.from_user.id, f"Выбрал этаж: {floor} (Офис: {office}, Город: {city})")

    rooms = DATA[city][office][floor].keys()
    markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=room)] for room in rooms] + [[KeyboardButton(text="⬅️ Назад")]],
        resize_keyboard=True
    )

    await message.answer(f"🛗 {floor}. Теперь выбери переговорную:", reply_markup=markup)

# 📌 Выбор переговорной с логированием
@dp.message(StateFilter(BookingState.choosing_room), F.text)
async def choose_room(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        user_data = await state.get_data()
        if "floor" in user_data:
            await choose_floor(message, state)
        else:
            await choose_office(message, state)
        return

    user_data = await state.get_data()
    city, office = user_data.get("city"), user_data.get("office")
    floor = user_data.get("floor", "")

    office_data = DATA.get(city, {}).get(office, {})
    rooms = office_data.get(floor, {}) if floor else office_data  

    if message.text not in rooms:
        return await message.answer("❌ Такой переговорной нет! Выберите из списка.")

    link = rooms[message.text]

    log_action(message.from_user.id, f"Разблокировал переговорную: {message.text} (Офис: {office}, Город: {city}, Этаж: {floor})")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔓 Разблокировать", url=link)]]
    )

    await message.answer("🔓 Нажмите кнопку для разблокировки:", reply_markup=keyboard)
    await state.set_state(BookingState.choosing_room)

# 📌 Запуск бота
async def main():
    logging.basicConfig(level=logging.INFO)
    print("🟢 Бот запущен! Теперь ВСЁ логируется 🚀")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())