from flask import Flask, jsonify
import requests

app = Flask(__name__)

USERNAME = '881101381017'
PASSWORD = '896811296068'
BASE_URL = f'http://solutta.shop:80/player_api.php?username={USERNAME}&password={PASSWORD}'

@app.route('/categorias', methods=['GET'])
def categorias():
    try:
        # URLs das categorias de filmes e séries
        url_vod = f'{BASE_URL}&action=get_vod_categories'
        url_series = f'{BASE_URL}&action=get_series_categories'

        # Requisições
        vod_response = requests.get(url_vod, timeout=10)
        series_response = requests.get(url_series, timeout=10)

        vod_data = vod_response.json() if vod_response.status_code == 200 else []
        series_data = series_response.json() if series_response.status_code == 200 else []

        # Combinar e remover duplicatas por nome
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
        return jsonify({'erro': 'Não foi possível carregar as categorias', 'detalhes': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
