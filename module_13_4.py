from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

api = '8140100256:AAGlB6QrZxAJ3vB6hyJ4eTcDLZocykdXAVU'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())



class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    activ = State()

@dp.message_handler(text= 'Calories')
async def send_activ(message):
    await message.answer('Оцените свою дневную активность и напиши получившееся число\n Если у тебя:\n '
                         'минимальная активность - 1.2\n слабая активность - 1.375\n средняя активность - 1.55\n'
                         ' высокая активность - 1.725\n экстр- активность - 1.9')
    await UserState.activ.set()

@dp.message_handler(state=UserState.activ)
async def set_age(message, state):
    await state.update_data(activ=message.text)
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await message.answer(f"Ваша норма калорий: {(10*int(data['weight'])+6.25*int(data['growth'])-5*int(data['age'])+5)*float(data['activ'])}")

    await state.finish()

@dp.message_handler(commands='start')
async def start(message):
    await message.answer(f'Привет! Я бот помогающий твоему здоровью.')

@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
