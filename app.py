from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random

app = Flask(__name__)

CITATY = [
    {"text": "Jediný spôsob, ako robiť skvelú prácu, je milovať to, čo robíš.", "autor": "Steve Jobs"},
    {"text": "Život nie je o tom, čakať kým búrka pominie, ale naučiť sa tancovať v daždi.", "autor": "Vivian Greene"},
    {"text": "Úspech je súčet malých snažení opakovaných deň čo deň.", "autor": "Robert Collier"},
    {"text": "Neuróbte z hory krtinca. Ale ak to urobíte, môžete na ňu vyliezť.", "autor": "neznámy"},
    {"text": "Každý deň je nová príležitosť byť lepším ako včera.", "autor": "neznámy"},
    {"text": "Sny sa nestanú skutočnosťou samy od seba. Musíte vstať a pracovať na nich.", "autor": "neznámy"},
    {"text": "Padnúť je dovolené. Vstať je povinné.", "autor": "neznámy"},
    {"text": "Najlepší čas zasadiť strom bol pred 20 rokmi. Druhý najlepší čas je teraz.", "autor": "čínske príslovie"},
    {"text": "Cesta tisíc míľ začína jediným krokom.", "autor": "Lao Tzu"},
    {"text": "Buďte zmenou, ktorú chcete vidieť vo svete.", "autor": "Mahatma Gandhi"},
]

@app.route('/')
def home():
    return jsonify({'status': 'ok'})

@app.route('/cas')
def cas():
    now = datetime.now()
    return jsonify({
        'cas': now.strftime('%H:%M'),
        'datum': now.strftime('%d.%m.%Y')
    })

@app.route('/pocasie')
def pocasie():
    api_key = "bd5e378503939ddaee76f12ad7a97608"
    r = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q=Trnava,SK&appid={api_key}&units=metric&lang=sk"
    )
    data = r.json()
    return jsonify({
        'teplota': round(data['main']['temp']),
        'popis': data['weather'][0]['description']
    })

@app.route('/biketower')
def biketower():
    try:
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        session.get('https://www.biketower.cz', headers=headers, timeout=10)
        r = session.get('https://www.biketower.cz/obsazenost_trnava_nadrazi/', headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        adult = soup.find('div', class_='obsazenost--value adult')
        kid = soup.find('div', class_='obsazenost--value kid')
        return jsonify({
            'dospela_volne': adult.text.strip() if adult else '?',
            'detske_volne': kid.text.strip() if kid else '?',
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/citat')
def citat():
    c = random.choice(CITATY)
    return jsonify(c)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
