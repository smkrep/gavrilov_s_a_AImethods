from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import yaml

np.random.seed(1337)
torch.manual_seed(1337)

# Подгрузка .env
load_dotenv()

# Подгрузка конфига с основными параметрами модели
with open("./config.yaml", "r") as cfg:
    default_values = yaml.safe_load(cfg)

#Инициализация Flask-приложения
app = Flask(__name__)

# Эндпоинт, принимающий POST-запрос от клиента на генерацию
# Возвращает json-строку со сгенерированным текстом
@app.route('/generate', methods=['POST'])
def generate_text():

    try:
        # Обработка случая, когда payload отсутствует
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Инициализация модели
        model_name_or_path = os.getenv(data["model"].upper())
        tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        model = AutoModelForCausalLM.from_pretrained(model_name_or_path)

        # Токенизация промпта
        input_ids = tokenizer.encode(data["prompt"], return_tensors="pt")

        # Генерация текста
        out = model.generate(input_ids, max_length=default_values["max_length"], temperature=default_values["temperature"], top_k=default_values["top_k"], top_p = default_values["top_p"],
                            num_return_sequences = default_values["num_options"], no_repeat_ngram_size = default_values["no_repeat_ngram"], do_sample=default_values["do_sample"])
        generated_list = list(map(tokenizer.decode, out))
        
        if data["model"].lower() == "llama":  
            return jsonify({
                "text": generated_list[0][17:]
            }), 200
        else:
            return jsonify({
                "text": generated_list[0]
            }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Запуск Flask-сервера
if __name__ == '__main__':
    app.run(debug=True, host=os.getenv('HOST'), port=os.getenv('PORT'))