import requests
import os
import sqlite3

from flask import Flask, jsonify
from dotenv import load_dotenv
from polygon import StocksClient

# load environment variables from .env file
load_dotenv()
app = Flask(__name__)

query_type = 'TIME_SERIES_INTRADAY'
symbol = 'IBM'
interval = '20min'
api_key_alpha_vantage = os.getenv('API_KEY_ALPHA_VANTAGE')
api_key_polygon_ai = os.getenv('API_KEY_POLYGON_AI')
polygon_client = StocksClient(api_key_polygon_ai)
local_db_path = os.getenv('DB_LOCATION')

@app.route('/')
def home():
    return jsonify(message="Hello, Flask!")


@app.route('/multiply/<int:x>/<int:y>')
def multiply(x, y):
    result = x * y
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/get-all-securities')
def get_all_securities():
    url = f'https://www.alphavantage.com/query?function={query_type}&symbol={symbol}&interval={interval}&apikey={api_key_alpha_vantage}'
    r = requests.get(url)
    data = r.json()
    if 'Error Message' in data:
        return jsonify(message=data['Error Message'])

    append_to_db(data)
    return jsonify(message=data)

@app.route('/get-all-securities-polygon')
def get_all_securities_polygon():
    tickers = []
    for t in polygon_client.list_tickers(
            market="stocks",
            active="true",
            order="asc",
            limit="100",
            sort="ticker",
    ):
        tickers.append(t)
        append_to_db(tickers)

def append_to_db(data_list):
    conn = sqlite3.connect(local_db_path)
    c = conn.cursor()
    c.executemany("INSERT INTO tickers (symbol, exchange) VALUES (?, ?)", data_list)
    conn.commit()
    conn.close()
