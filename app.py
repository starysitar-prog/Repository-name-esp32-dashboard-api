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
        headers = {
            'User-Agent': 'Mozilla/5.0',
        }
        now = datetime.now()
        url = "https://idos.idnes.cz/vlakyautobusymhd/spojeni/"
        params = {
            'f': 'Trnava',
            't': 'Bratislava',
            'date': now.strftime('%d.%m.%Y'),
            'time': now.strftime('%H:%M'),
        }
        r = requests.get(url, params=params, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        spoje = []
        rows = soup.select('.connection-list li.item')[:5]
        for row in rows:
            odchod = row.select_one('.time-array .departure')
            prichod = row.select_one('.time-array .arrival')
            if odchod and prichod:
                spoje.append({
                    'odchod': odchod.text.strip(),
                    'prichod': prichod.text.strip(),
                })
        
        return jsonify({
            'spoje': spoje,
            'html_snippet': r.text[5000:7000]
        })
    except Exception as e:
        return jsonify({'error': str(e)})
