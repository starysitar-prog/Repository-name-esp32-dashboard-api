from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

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

@app.route('/vlaky')
def vlaky():
    try:
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://cp.sk/',
        }
        now = datetime.now()
        params = {
            'From': 'Trnava',
            'FromHidden': 'Trnava%1%14141',
            'To': 'Bratislava',
            'ToHidden': 'Bratislava%1%1371',
            'Date': now.strftime('%d.%m.%Y'),
            'Time': now.strftime('%H:%M'),
            'IsArr': 'False',
            'OnlyDirect': 'False',
        }
        r = session.post('https://cp.sk/vlakbusmhd/spojenie/', data=params, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        return jsonify({
            'html_snippet': r.text[6000:8000]
        })
    except Exception as e:
        return jsonify({'error': str(e)})
