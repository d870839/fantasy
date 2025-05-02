from flask import Flask, render_template, request, jsonify
import requests
import certifi
import sqlite3
import os

app = Flask(__name__)
DB_PATH = 'league.db'

# Replace with your values
LEAGUE_ID = '2005813'
SEASON = '2024'
SWID = '{BB347049-4815-4607-9D9F-D7A4D188AFA2}'
ESPN_S2 = 'AECb%2FGmhFO0j3b6PvxaiLiChA3OYpSKewwXJ4Dz%2BZfkOafErF6%2FYbmAV4aAiL961pFmW%2BWTWMdY75kP09D7%2BDWNeh4vAL2pWvCA4v8%2BxBuU1c%2BzquBXIpbw%2F4OgKvyn7nqaAhMOo1OvwvXgJThgb4t74rSSrVMM3Jlog%2B5LcNVwiJwHes3HlbWz8t%2Bd8LNx4mLcuP3yQ4xvmwmRdaLSP%2Bf6hzkSRsVET9lKUAZxKCfjCRwBiNIWyWR4rC94PiGJYwiHatrafV6DJpoH%2BFwT7O%2F%2BLMn6S%2BkyTQydj1QHDbYu76g%3D%3D'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch', methods=['GET'])
def fetch_data():
    response = requests.get(
    f"https://fantasy.espn.com/apis/v3/games/ffl/seasons/2024/segments/0/leagues/YOUR_LEAGUE_ID",
    cookies = {
    'swid': os.getenv("SWID"),
    'espn_s2': os.getenv("ESPN_S2")
},
    verify=certifi.where()  # ✅ Ensures proper cert chain
)
    data = response.json()

    # Example: extract team names
    teams = [{'name': team['location'] + ' ' + team['nickname']} for team in data['teams']]
    return jsonify(teams)

if __name__ == '__main__':
    app.run(debug=True)
