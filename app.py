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
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'sk,cs;q=0.9,en;q=0.8',
        }
        r = requests.get('https://www.biketower.cz/obsazenost_trnava_nadrazi/', headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        adult = soup.find('div', class_='obsazenost--value adult')
        kid = soup.find('div', class_='obsazenost--value kid')
        
        adult_spans = adult.find_all('span') if adult else []
        kid_spans = kid.find_all('span') if kid else []
        
        return jsonify({
            'dospela_volne': adult_spans[0].text if len(adult_spans) > 0 else '?',
            'dospela_celkom': adult_spans[1].text if len(adult_spans) > 1 else '?',
            'detske_volne': kid_spans[0].text if len(kid_spans) > 0 else '?',
            'detske_celkom': kid_spans[1].text if len(kid_spans) > 1 else '?',
        })
    except Exception as e:
        return jsonify({'error': str(e)})
