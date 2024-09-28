import requests
import tkinter as tk
from tkinter import scrolledtext
from copy import deepcopy
from dotenv import load_dotenv
import os

load_dotenv()

#Pipeline: ru -> es -> de -> tr -> ru
#Test string 1: Когда за околицей щурится утренник, словно старый вереск в непролазных чащах, ходит молва, что ежели не приметишь дорожку подле каменной гряды, то сам будешь искать свой след до самых косых сумерек
#Test string 2: А ежели приспичит кликнуть ворона, знай, вертится карачун где-то поблизости — до беды рукой подать
#Test string 3: Он сидел на завалинке, глядя вдаль, как бабье лето мягко стелилось по земле. В воздухе витал запах скошенной травы, и ветерок играл с одинокими осенними листьями, словно пытаясь их задержать, хотя время неумолимо двигалось вперёд. Где-то далеко слышался гул трактора, а в душе поселилась тоскливая светлая грусть, которая бывает только на закате золотой осени.

def google_translation_pipeline(text):

    url_google = os.getenv('GOOGLE_URL')
    headers_google = {
    	"x-rapidapi-key": os.getenv('RAPIDAPI_KEY'),
    	"x-rapidapi-host": os.getenv('GOOGLE_RAPIDAPI_HOST'),
    	"Content-Type": "application/json"
    }

    languages = ["ru", "es", "de", "tr", "ru"]

    for fr, to in zip(languages[:-1], languages[1:]):
        payload_google = {
            "from": fr,
            "to": to,
            "text": text
        }
        response_google = requests.post(url_google, json=payload_google, headers=headers_google)
        text = response_google.json()["trans"]

    return text

    
def deepl_translation_pipeline(text):
    url = os.getenv('DEEPL_URL')

    headers = {
    	"x-rapidapi-key": os.getenv('RAPIDAPI_KEY'),
    	"x-rapidapi-host": os.getenv('DEEPL_RAPIDAPI_HOST'),
    	"Content-Type": "application/json"
    }

    languages = ["ru", "es", "de", "tr", "ru"]

    for fr, to in zip(languages[:-1], languages[1:]):
        payload = {
            "q": text,
            "source": fr,
            "target": to
        }
        response = requests.post(url, json=payload, headers=headers)
        text = response.json()["data"]["translations"]["translatedText"]

    return text


def display_text():
    input_text = input_box.get("1.0", tk.END)

    google_box.delete(1.0, tk.END)  
    deepl_box.delete(1.0, tk.END)

    ans_google = google_translation_pipeline(deepcopy(input_text))
    google_box.insert(tk.END, ans_google)
    
    ans_deepl = deepl_translation_pipeline(deepcopy(input_text))
    deepl_box.insert(tk.END, ans_deepl)  

root = tk.Tk()
root.title("Lab1 (translation comparison)")
root.geometry("800x600")

input_label = tk.Label(root, text="Input")
input_label.pack(pady=5)
input_box = scrolledtext.ScrolledText(root, width=70, height=5)
input_box.pack(pady=10)  

button = tk.Button(root, text="Run test", command=display_text)
button.pack(pady=5)

google_label = tk.Label(root, text="Google Translate")
google_label.pack(pady=5)
google_box = scrolledtext.ScrolledText(root, width=90, height=8)
google_box.pack(pady=10)

deepl_label = tk.Label(root, text="DeepL Translate")
deepl_label.pack(pady=5)
deepl_box = scrolledtext.ScrolledText(root, width=90, height=8)
deepl_box.pack(pady=10)

root.mainloop()

