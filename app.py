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
        teams = [{
            "id": team.team_id,  # Add this
            "name": team.team_name,
            "owner": team.owners[0].get("displayName", "Unknown")
        } for team in league.teams]

        app.logger.info(f"Successfully pulled {len(teams)} teams.")
        return jsonify(teams)
    except Exception as e:
        app.logger.error("Error fetching league data:")
        app.logger.error(str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/history')
def fetch_matchup_history():
    from espn_api.football import League
    league_id = 2005813
    season = 2023
    swid = os.getenv("SWID")
    espn_s2 = os.getenv("ESPN_S2")

    try:
        league = League(league_id=league_id, year=season, swid=swid, espn_s2=espn_s2)
        data = []

        for team in league.teams:
            matchups = []
            wins = 0
            losses = 0
            best_margin = None
            worst_loss = None

            for matchup in team.schedule:
                if matchup is None or matchup.opponent is None:
                    continue  # skip bye weeks or null data

                week = matchup.period
                points = matchup.points
                projected = matchup.projected_points
                opp_name = matchup.opponent.team_name
                opp_points = matchup.opponent.points
                won = matchup.winner == 'WIN'
                margin = round(points - opp_points, 2)

                # Update W-L
                if won:
                    wins += 1
                    if best_margin is None or margin > best_margin:
                        best_margin = margin
                else:
                    losses += 1
                    if worst_loss is None or margin < worst_loss:
                        worst_loss = margin

                matchups.append({
                    "week": week,
                    "points": points,
                    "projected": projected,
                    "opponent": opp_name,
                    "opponent_points": opp_points,
                    "won": won,
                    "margin": margin
                })

            team_data = {
                "name": team.team_name,
                "owner": team.owners[0].get("displayName", "Unknown"),
                "wins": wins,
                "losses": losses,
                "best_margin": best_margin,
                "worst_loss": worst_loss,
                "matchups": matchups
            }

            data.append(team_data)

        return jsonify(data)
    except Exception as e:
        app.logger.error("Error fetching matchup history:")
        app.logger.error(str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/history/all-seasons')
def fetch_all_season_stats():
    from espn_api.football import League
    league_id = 2005813
    swid = os.getenv("SWID")
    espn_s2 = os.getenv("ESPN_S2")
    all_seasons = []

    for season in range(2018, 2024):  # Adjust range based on your league's age
        try:
            league = League(league_id=league_id, year=season, swid=swid, espn_s2=espn_s2)
            app.logger.info(f"Processing season {season}...")
            season_data = {
                "season": season,
                "teams": []
            }

            for team in league.teams:
                matchups = []
                wins = 0
                losses = 0
                best_margin = None
                worst_loss = None

                for matchup in team.schedule:
                    if matchup is None or matchup.opponent is None:
                        continue

                    margin = round(matchup.points - matchup.opponent.points, 2)
                    won = matchup.winner == 'WIN'

                    if won:
                        wins += 1
                        best_margin = margin if best_margin is None else max(best_margin, margin)
                    else:
                        losses += 1
                        worst_loss = margin if worst_loss is None else min(worst_loss, margin)

                team_data = {
                    "name": team.team_name,
                    "owner": team.owners[0].get("displayName", "Unknown"),
                    "wins": wins,
                    "losses": losses,
                    "best_margin": best_margin,
                    "worst_loss": worst_loss
                }
                season_data["teams"].append(team_data)

            all_seasons.append(season_data)
        except Exception as e:
            app.logger.warning(f"Skipping season {season}: {e}")
            continue

    return jsonify(all_seasons)


@app.route('/view-history')
def view_history():
    return render_template('history.html')

@app.route('/view-history/all')
def view_all_history():
    return render_template('all_seasons.html')

@app.route('/team/<int:team_id>')
def view_team_history(team_id):
    return render_template('team_history.html', team_id=team_id)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render provides this env var
    app.run(host='0.0.0.0', port=port)