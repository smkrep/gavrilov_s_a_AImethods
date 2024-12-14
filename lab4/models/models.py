import aiohttp
import os

#Функция, которая отправляет пользовательский промпм на сервер с моделью
#Аргументы:
# prompt - пользовательский промпт
# model - тип модели для генерации
# Возвращает строку с ответом модели
async def get_text(prompt: str, model: str) -> str:

    url = f"http://{os.getenv('HOST')}:{os.getenv('PORT')}/generate"

    payload = {'prompt': prompt, 'model': model}

    async with aiohttp.ClientSession() as session:
        try:
            #Отправка POST-запроса и получение ответа
            async with session.post(url, json=payload) as response:
                response_data = await response.json()
                return response_data["text"]
        except aiohttp.ClientError as e:
            print(f"Request to {url} failed: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")