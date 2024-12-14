from aiogram.utils.keyboard import InlineKeyboardBuilder


# Функция, создающая клавиатуру для выбора модели
# Возвращает созданную inline-клавиатуру
def get_choose_model_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="GPT", callback_data="choose_gpt")
    builder.button(text="Llama", callback_data="choose_llama")
    return builder.as_markup()


# Функция, создающая клавиатуру для ввода промпта
# Возвращает созданную inline-клавиатуру
def get_input_prompt_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Назад", callback_data="go_back")
    return builder.as_markup()


# Функция, создающая клавиатуру, показывающаяся после отправки промпта на генерацию
# Возвращает созданную inline-клавиатуру
def get_end_prompt_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Назад к моделям", callback_data="go_back_to_gen")
    builder.button(text="Завершить", callback_data="end_interaction")
    return builder.as_markup()


# Функция, создающая клавиатуру, показывающаяся после команды /start
# Возвращает созданную inline-клавиатуру
def get_start_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Начать", callback_data="do_start")
    return builder.as_markup()