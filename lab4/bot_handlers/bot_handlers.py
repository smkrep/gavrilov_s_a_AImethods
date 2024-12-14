import asyncio
from aiogram import Router
router = Router()

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from models.models import get_text
from keyboards.keyboards import get_choose_model_kb, get_input_prompt_kb, get_end_prompt_kb, get_start_kb
from aiogram_run import bot


#Класс, содержащий возможные состояния бота
class BotStates(StatesGroup):
    start_state = State()
    choose_model = State()  
    input_prompt = State()


# Обработчик команды /start
# Аргументы:
# callback - объект, содержащий информацию, передающуюся после нажатия кнопки на inline-клавиатуре
# message - сообщение от пользователя
@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await state.set_state(BotStates.start_state)
    await message.answer("Здравствуйте! Этот бот умеет продолжать переданный промпт на русском языке при помощи генерации текста моделью семейства Llama или GPT. Нажмите кнопку чтобы начать", reply_markup=get_start_kb())

# Обработчик нажатия кнопки "Начать"
# Аргументы:
# callback - объект, содержащий информацию, передающуюся после нажатия кнопки на inline-клавиатуре
# state - состояние, в котором находится FSM на момент запроса
@router.callback_query(lambda callback: callback.data == "do_start", BotStates.start_state)
async def start_button_pressed(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BotStates.choose_model)
    await callback.message.answer("Выберите языковую модель:", reply_markup=get_choose_model_kb())
    await callback.answer()


# Обработчик нажатия кнопок с названиями моделей
# Аргументы:
# callback - объект, содержащий информацию, передающуюся после нажатия кнопки на inline-клавиатуре
# state - состояние, в котором находится FSM на момент запроса
@router.callback_query(lambda callback: callback.data in ["choose_gpt", "choose_llama"], BotStates.choose_model)
async def choose_model(callback: CallbackQuery, state: FSMContext):
    model = "GPT" if callback.data == "choose_gpt" else "Llama"
    await state.update_data(model=model)
    await state.set_state(BotStates.input_prompt)
    await callback.message.answer(f"Вы выбрали модель: {model}. Введите ваш промпт:", reply_markup=get_input_prompt_kb())
    await callback.answer()


# Обработчик кнопки "Назад"
# Аргументы:
# callback - объект, содержащий информацию, передающуюся после нажатия кнопки на inline-клавиатуре
# state - состояние, в котором находится FSM на момент запроса
@router.callback_query(lambda callback: callback.data == "go_back", BotStates.input_prompt)
async def go_back(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BotStates.choose_model)
    await callback.message.answer("Вы вернулись к выбору модели:", reply_markup=get_choose_model_kb())
    await callback.answer()


# Обработчик ввода промпта
# Аргументы:
# callback - объект, содержащий информацию, передающуюся после нажатия кнопки на inline-клавиатуре
# message - сообщение от пользователя (в данном случае промпт)
@router.message(BotStates.input_prompt)
async def input_prompt(message: Message, state: FSMContext):
    user_data = await state.get_data()
    model = user_data.get("model")
    await message.answer(f"Вы выбрали модель {model} с промптом: '{message.text}', выполняется генерация...")
    asyncio.create_task(handle_text_generation(message.text, model, message.chat.id))
    await message.answer("Выберите дальнейшее действие:", reply_markup=get_end_prompt_kb())


# Обработчик нажатия на кнопку завершения взаимодействия
# Аргументы:
# callback - объект, содержащий информацию, передающуюся после нажатия кнопки на inline-клавиатуре
@router.callback_query(lambda callback: callback.data == "end_interaction")
async def end_interaction(callback: CallbackQuery):
    await callback.message.answer("Спасибо за использование бота, до свидания!")
    await callback.answer()


# Обработчик нажатия кнопки "Назад" после генерации
# Аргументы:
# callback - объект, содержащий информацию, передающуюся после нажатия кнопки на inline-клавиатуре
# state - состояние, в котором находится FSM на момент запроса
@router.callback_query(lambda callback: callback.data == "go_back_to_gen", BotStates.input_prompt)
async def go_back_after_generation(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BotStates.choose_model)
    await callback.message.answer("Вы вернулись к выбору модели. Выберите нужную вам модель для генерации: ", reply_markup=get_choose_model_kb())
    await callback.answer()


# Функция, ожидающая ответа со сгенерированным текстом и отправляющая полученный ответ тому, кто сделал запрос
# Аргументы:
# prompt - пользовательский промпт, к которому генерируется дополнение
# model - тип модели, которая будет генерировать ответ
# chat_id - id чата, в который надо отправить сгенерированный текст
async def handle_text_generation(prompt: str, model: str, chat_id: int):
    generated_text = await get_text(prompt, model)
    await bot.send_message(chat_id, f"Ответ на промпт '{prompt}', сгенерированный моделью семейства {model}:\n\n{generated_text}")