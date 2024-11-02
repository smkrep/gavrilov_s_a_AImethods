from model import generate_text
import tkinter as tk
from tkinter import scrolledtext
import yaml

#Подгрузка конфига
with open("./lab2/config.yaml", "r") as cfg:
    default_values = yaml.safe_load(cfg)


#Функция, которая считывает значения из полей ввода интерфейса, передает их в модель для генерации текста и выводит
#сгенерированный текст в поле output_text
def on_generate_button_click():

    #Очистка поля вывода
    output_text.delete("1.0", tk.END)

    #Получение данных из полей ввода
    prompt = input_prompt.get()
    max_len = int(max_length.get())
    temp = float(temperature.get())
    topk = int(top_k.get())
    topp = float(top_p.get())
    options = int(num_options.get())
    no_repeat = int(no_repeat_ngram.get())
    sampling_flag = bool(use_sampling_flag.get())
    
    #Получение массива сгенерированных текстов
    generated_sequences = generate_text(model_type=default_values["model"], prompt=prompt, max_len=max_len, temp=temp, topk=topk, topp=topp,
                                       options=options, no_repeat=no_repeat, sampling_flag=sampling_flag)
    
    #Заполнение строки с ответом
    text_to_view = ""
    for index in range(len(generated_sequences)):
        text_to_view += f"Вариант №{index+1}:\n{generated_sequences[index]}\n\n"

    #Вывод строки с ответом в соответствующее поле
    output_text.insert("1.0", text_to_view)
        

#Функция, инициализирующая графический интерфейс приложения
def start_frontend():
    root.mainloop()

#Создание окна интерфейса
root = tk.Tk()
root.title("Оценка генерации текста")
root.geometry("700x700")

#Создание сетки
frame = tk.Frame(root)
frame.pack(pady=10, padx=10, fill="x")


#Создание поля ввода стартового промпта
tk.Label(frame, text="Стартовая фраза:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
input_prompt = tk.Entry(frame, width=90)
input_prompt.insert(0, "К югу от Москвы расположен город")
input_prompt.grid(row=0, column=1, padx=5, pady=5)

#Создание поля ввода максимальной длины ответа
tk.Label(frame, text="Максимальная длина ответа:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
max_length = tk.Entry(frame, width=35)
max_length.insert(0, default_values["max_length"])
max_length.grid(row=1, column=1, padx=5, pady=5)

#Создание поля ввода температуры
tk.Label(frame, text="Температура:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
temperature = tk.Entry(frame, width=35)
temperature.insert(0, default_values["temperature"])
temperature.grid(row=2, column=1, padx=5, pady=5)

#Создание поля ввода top_k
tk.Label(frame, text="Значение top_k:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
top_k = tk.Entry(frame, width=35)
top_k.insert(0, default_values["top_k"])
top_k.grid(row=3, column=1, padx=5, pady=5)

#Создание поля ввода top_p
tk.Label(frame, text="Значение top_p:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
top_p = tk.Entry(frame, width=35)
top_p.insert(0, default_values["top_p"])
top_p.grid(row=4, column=1, padx=5, pady=5)

#Создание поля ввода количества генераций
tk.Label(frame, text="Количество генераций:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
num_options = tk.Entry(frame, width=35)
num_options.insert(0, default_values["num_options"])
num_options.grid(row=5, column=1, padx=5, pady=5)

#Создание поля ввода размера неповторяемых n-грамм
tk.Label(frame, text="Размер неповторяемых n-грамм:").grid(row=6, column=0, sticky="w", padx=5, pady=5)
no_repeat_ngram = tk.Entry(frame, width=35)
no_repeat_ngram.insert(0, default_values["no_repeat_ngram"])
no_repeat_ngram.grid(row=6, column=1, padx=5, pady=5)

#Создание чекбокса флага семплирования
use_sampling_flag = tk.BooleanVar(value=default_values["do_sample"])
sampling_checkbox = tk.Checkbutton(frame, text="Семплировать", variable=use_sampling_flag)
sampling_checkbox.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

#Создание кнопки "Сгенерировать"
generate_button = tk.Button(frame, text="Сгенерировать", command=on_generate_button_click, width=70)
generate_button.grid(row=8, column=0, columnspan=2, pady=10)

#Создание поля вывода ответа модели
output_text = scrolledtext.ScrolledText(root, wrap="word", height=70, width=90)
output_text.pack(padx=10, pady=(0, 10))




