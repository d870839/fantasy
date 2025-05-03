from flask import Flask, render_template, jsonify
from espn_api.football import League
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch')
def fetch_teams():
    league_id = 2005813  # Replace with your league ID
    season = 2023        # Use current or past season

    swid = os.getenv("SWID")
    espn_s2 = os.getenv("ESPN_S2")

    try:
        league = League(league_id=league_id, year=season, espn_s2=espn_s2, swid=swid)
        teams = [{"name": team.team_name, "owner": team.owner} for team in league.teams]
        return jsonify(teams)
    except Exception as e:
        app.logger.error(f"Failed to fetch league: {e}")
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render provides this env var
    app.run(host='0.0.0.0', port=port)