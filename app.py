from flask import Flask, render_template, request, jsonify
import requests
import certifi
import sqlite3
import os
import logging

# Ensure logs go to stdout so Render sees them
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
DB_PATH = 'league.db'

# Replace with your values
LEAGUE_ID = '2005813'
SEASON = '2024'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch')
def fetch_data():
    import os, certifi
    url = f'https://fantasy.espn.com/apis/v3/games/ffl/seasons/{SEASON}/segments/0/leagues/{LEAGUE_ID}'
    
    cookies = {
        'swid': os.getenv("SWID"),
        'espn_s2': os.getenv("ESPN_S2")
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    response = requests.get(url, cookies=cookies, headers=headers, verify=certifi.where())

    app.logger.info(f"Status code from ESPN: {response.status_code}")
    app.logger.info(f"Response preview: {response.text[:500]}")

    try:
        data = response.json()
        return jsonify(data)
    except Exception:
        app.logger.error("Failed to parse ESPN response as JSON.")
        return jsonify({
            "error": "Invalid response from ESPN",
            "status": response.status_code,
            "text": response.text[:300]
        }), 500





if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render provides this env var
    app.run(host='0.0.0.0', port=port)