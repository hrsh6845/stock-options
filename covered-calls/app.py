import requests
import os
import sqlite3

from flask import Flask, jsonify
from dotenv import load_dotenv
from polygon import StocksClient

# load environment variables from .env file
load_dotenv()
app = Flask(__name__)

# pull keys from environment variables.
api_key_alpha_vantage = os.getenv('API_KEY_ALPHA_VANTAGE')
api_key_polygon_ai = os.getenv('API_KEY_POLYGON_AI')
local_db_path = os.getenv('DB_LOCATION')

# local initializations.
polygon_client = StocksClient(api_key=api_key_polygon_ai)

@app.route('/')
def home():
    return jsonify(message="Hello, Flask!")

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/get-all-securities')
def get_all_securities():
    tickers = []
    count = 0
    url = f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit=100&sort=ticker&apiKey={api_key_polygon_ai}'

    while True:
        r = requests.get(url + f'&apiKey={api_key_polygon_ai}')
        data = r.json()
        count += 1
        url = data['next_url']
        for t in data['results']:
            tickers.append((t['ticker'], t['primary_exchange']))
        if count >= 5:
            break

    initial_security_append(tickers)
    return jsonify(message=data)

def initial_security_append(data_list):
    conn = sqlite3.connect(local_db_path)
    c = conn.cursor()
    c.executemany("INSERT OR IGNORE INTO tickers (symbol, exchange) VALUES (?, ?)", data_list)
    conn.commit()
    conn.close()

@app.route('/monday-suggestions')
def monday_suggestions():
    # pull options data for all the securities
    return