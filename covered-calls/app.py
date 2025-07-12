import requests
import os

from flask import Flask, jsonify
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()
app = Flask(__name__)

query_type = 'TIME_SERIES_INTRADAY'
symbol = 'IBM'
interval = '20min'
api_key = os.getenv('API_KEY')

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

    url = f'https://www.alphavantage.co/query?function={query_type}&symbol={symbol}&interval={interval}&apikey={api_key}'
    r = requests.get(url)
    data = r.json()
    if 'Error Message' in data:
        return jsonify(message=data['Error Message'])

    return jsonify(message=data)