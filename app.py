@app.route('/biketower')
def biketower():
    try:
        r = requests.get('https://www.biketower.cz/obsazenost_trnava_nadrazi/', timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Hladame obsadenost
        obsadenost = soup.find('div', class_='obsazenost')
        volne = soup.find('div', class_='volne')
        celkom = soup.find('div', class_='celkem')
        
        # Ziskame vsetky cisla zo stranky
        import re
        text = soup.get_text()
        cisla = re.findall(r'\d+', text[:2000])
        
        return jsonify({
            'status': 'V PROVOZU' if 'V PROVOZU' in text else 'MIMO PROVOZ',
            'cisla': cisla[:20],
            'raw': text[400:800]
        })
    except Exception as e:
        return jsonify({'error': str(e)})
