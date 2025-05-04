from flask import Flask, render_template, jsonify
from espn_api.football import League
import os
import logging

# Configure logging so Render shows INFO and ERROR logs
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch')
def fetch_teams():
    from espn_api.football import League
    league_id = 2005813
    season = 2023
    swid = os.getenv("SWID")
    espn_s2 = os.getenv("ESPN_S2")

    try:
        app.logger.info("Attempting to connect to ESPN League API...")
        league = League(league_id=league_id, year=season, swid=swid, espn_s2=espn_s2)
        teams = [{"name": team.team_name, "owner": str(team.owners[0])} for team in league.teams]
        app.logger.info(f"Successfully pulled {len(teams)} teams.")
        return jsonify(teams)
    except Exception as e:
        app.logger.error("Error fetching league data:")
        app.logger.error(str(e))
        return jsonify({"error": str(e)}), 500




if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render provides this env var
    app.run(host='0.0.0.0', port=port)