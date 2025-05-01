from flask import Flask, render_template, request, jsonify
import requests
import sqlite3
import os

app = Flask(__name__)
DB_PATH = 'league.db'

# Replace with your values
LEAGUE_ID = 'YOUR_LEAGUE_ID'
SEASON = '2024'
SWID = '{YOUR_SWID}'
ESPN_S2 = 'YOUR_ESPN_S2'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch', methods=['GET'])
def fetch_data():
    url = f'https://fantasy.espn.com/apis/v3/games/ffl/seasons/{SEASON}/segments/0/leagues/{LEAGUE_ID}'
    cookies = {'swid': SWID, 'espn_s2': ESPN_S2}
    r = requests.get(url, cookies=cookies)
    data = r.json()

    # Example: extract team names
    teams = [{'name': team['location'] + ' ' + team['nickname']} for team in data['teams']]
    return jsonify(teams)

if __name__ == '__main__':
    app.run(debug=True)
