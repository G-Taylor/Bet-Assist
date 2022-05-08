from flask import Flask, render_template, request
from data_retrieval.Main import get_suggested_matches
from data_retrieval.game_fixtures_and_results import *
from data_retrieval.league_urls import *
from data_retrieval.league_ids import *
from data_retrieval.league_logos import *

app = Flask(__name__)


# App Route for the index page of the application
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# App Route for the Over 2.5 goals games page of the application
@app.route('/over2', methods=['GET', 'POST'])
def over2():
    current_league = "Premiership"
    league, table_id, logo = set_league_info(current_league)

    if request.method == "POST":
        current_league = request.form.get('league')
        league, table_id, logo = set_league_info(current_league)

    results = reset_and_get_new_league_values(league)

    return render_template('over2.html',
                           results=results,
                           current_league=current_league,
                           current_standings=current_standings,
                           table_id=table_id,
                           logo=logo
                           )


# App Route for the BTTS games page of the application
@app.route('/btts', methods=['GET', 'POST'])
def btts():
    current_league = "Premiership"
    league, table_id, logo = set_league_info(current_league)

    if request.method == "POST":
        current_league = request.form.get('league')
        league, table_id, logo = set_league_info(current_league)

    results = reset_and_get_new_league_values(league)

    return render_template('btts.html',
                           results=results,
                           current_league=current_league,
                           current_standings=current_standings,
                           table_id=table_id,
                           logo=logo
                           )


# App Route for the all games page of the application
@app.route('/all_games', methods=['GET', 'POST'])
def all_games():
    current_league = "Premiership"
    league, table_id, logo = set_league_info(current_league)

    if request.method == "POST":
        current_league = request.form.get('league')
        league, table_id, logo = set_league_info(current_league)

    results = reset_and_get_new_league_values(league)

    return render_template('all_games.html',
                           results=results,
                           current_league=current_league,
                           current_standings=current_standings,
                           table_id=table_id,
                           logo=logo
                           )


def set_league_info(current_league):
    league = f"{WEBSITE_URL}{leagues[current_league]}"
    table_id = league_ids[current_league]
    logo = league_logos[current_league]

    return league, table_id, logo


def reset_and_get_new_league_values(league):
    reset_all_value_stores()
    get_games_played(f"{league}results/")
    get_fixtures(f"{league}fixtures/")
    get_current_standings(f"{league}standings/")
    convert_data()

    total_goals_scored_dict = merge_dict(home_goals_scored_dict, away_goals_scored_dict)
    total_goals_conceded_dict = merge_dict(home_goals_conceded_dict, away_goals_conceded_dict)
    all_results_dict = merge_dict(away_team_results_dict, home_team_results_dict)

    results = get_suggested_matches(total_goals_scored_dict, total_goals_conceded_dict, all_results_dict)

    return results


if __name__ == '__main__':
    app.run(debug=True)
