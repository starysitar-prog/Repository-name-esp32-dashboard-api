from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random

app = Flask(__name__)

CITATY = [
    {"text": "Jediny sposob, ako robit skvelu pracu, je milovat to, co robis.", "autor": "Steve Jobs"},
    {"text": "Zivot nie je o tom, cakat kym burka pominie, ale naucit sa tancovat v dazdi.", "autor": "Vivian Greene"},
    {"text": "Uspech je sucet malych snazeni opakovanych den co den.", "autor": "Robert Collier"},
    {"text": "Neurobte z hory krtinca. Ale ak to urobite, mozete na nu vyliezt.", "autor": "neznamy"},
    {"text": "Kazdy den je nova prilezitost byt lepsim ako vcera.", "autor": "neznamy"},
    {"text": "Sny sa nestanu skutocnostou same od seba. Musite vstat a pracovat na nich.", "autor": "neznamy"},
    {"text": "Padnut je dovolene. Vstat je povinne.", "autor": "neznamy"},
    {"text": "Najlepsi cas zasadit strom bol pred 20 rokmi. Druhy najlepsi cas je teraz.", "autor": "cinske prislovie"},
    {"text": "Cesta tisic mil zacina jedinym krokom.", "autor": "Lao Tzu"},
    {"text": "Budte zmenou, ktoru chcete vidiet vo svete.", "autor": "Mahatma Gandhi"}
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
