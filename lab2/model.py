import numpy as np
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from typing import List

#Сидирование генератора случайных чисел
np.random.seed(42)
torch.manual_seed(42)

#Функция, осуществляющая генерацию текста при помощи модели RuGPT3small
#Параметры:
#prompt - исходная промпт-строка
#max_len - максимальная длина генерируемой последовательности токенов
#temp - температура (модуляция вероятности следующего токена)
#topk - топ по вероятности токенов для использования
#topp - для генерации используются токены с кумулятивной вероятностью topp и более
#options - количество генерируемых последовательностей
#no_repeat - минимальная длина неповторяющейся последовательности слов
#sampling_flag - флаг, несущий информацию о необходимости семплирования
#Возвращаемое значение:
#Функция возвращает список сгенерированных текстов. Размер списка равен options
def generate_text(prompt: str, max_len: int, temp: float, topk: int, topp: float,
                options: int, no_repeat: int, sampling_flag: bool) -> List[str]:
    
    #Инициализация модели
    model_name_or_path = "sberbank-ai/rugpt3small_based_on_gpt2"
    tokenizer = GPT2Tokenizer.from_pretrained(model_name_or_path)
    model = GPT2LMHeadModel.from_pretrained(model_name_or_path)

    #Токенизация исходной промпт-строки
    input_ids = tokenizer.encode(prompt, return_tensors="pt")

    #Получение ответа в виде списка строк
    out = model.generate(input_ids, max_length=max_len, temperature=temp, top_k=topk, top_p = topp,
                        num_return_sequences = options, no_repeat_ngram_size = no_repeat, do_sample=sampling_flag)
    generated_list = list(map(tokenizer.decode, out))
    return generated_list