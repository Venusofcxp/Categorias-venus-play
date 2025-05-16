from flask import Flask, jsonify
import requests

app = Flask(__name__)

USERNAME = '881101381017'
PASSWORD = '896811296068'
BASE_URL = f'http://solutta.shop:80/player_api.php?username={USERNAME}&password={PASSWORD}'

@app.route('/api/categorias', methods=['GET'])
def categorias():
    try:
        url_vod = f'{BASE_URL}&action=get_vod_categories'
        url_series = f'{BASE_URL}&action=get_series_categories'

        vod_data = requests.get(url_vod, timeout=10).json()
        series_data = requests.get(url_series, timeout=10).json()

        categorias_unicas = {}
        for categoria in vod_data + series_data:
            nome = categoria.get('category_name')
            if nome and nome not in categorias_unicas:
                categorias_unicas[nome] = {
                    'category_id': categoria.get('category_id'),
                    'category_name': nome
                }

        return jsonify(list(categorias_unicas.values()))
    except Exception as e:
        return jsonify({'erro': 'Erro ao buscar categorias', 'detalhes': str(e)}), 500
