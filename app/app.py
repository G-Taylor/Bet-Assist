from flask import Flask, render_template, request
from data_retrieval.Main import get_suggested_matches
from data_retrieval.game_fixtures_and_results import *
from data_retrieval.league_urls import *
from data_retrieval.league_ids import *
from data_retrieval.league_logos import *
from flask_caching import Cache

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
# tell Flask to use the above defined config
app.config.from_mapping(config)
cache = Cache(app)


# App Route for the index page of the application
@app.route('/', methods=['GET', 'POST'])
@cache.cached(timeout=50)
def index():
    return render_template('index.html')


# App Route for the Over 2.5 goals games page of the application
@app.route('/over2/<cl>', methods=['GET', 'POST'])
@cache.cached(timeout=50)
def over2(cl):
    current_league = cl
    league, table_id, logo = set_league_info(current_league)

    results = reset_and_get_new_league_values(league)

    return render_template('over2.html',
                           res=results,
                           league=current_league,
                           standings=current_standings,
                           table_id=table_id,
                           logo=logo,
                           page='over2'
                           )


# App Route for the BTTS games page of the application
@app.route('/btts/<cl>', methods=['GET', 'POST'])
@cache.cached(timeout=50)
def btts(cl):
    current_league = cl
    league, table_id, logo = set_league_info(current_league)

    results = reset_and_get_new_league_values(league)

    return render_template('btts.html',
                           res=results,
                           league=current_league,
                           standings=current_standings,
                           table_id=table_id,
                           logo=logo,
                           page='btts'
                           )


# App Route for the all games page of the application
@app.route('/all_games/<cl>', methods=['GET', 'POST'])
@cache.cached(timeout=50)
def all_games(cl):
    current_league = cl
    league, table_id, logo = set_league_info(current_league)

    results = reset_and_get_new_league_values(league)

    return render_template('all_games.html',
                           res=results,
                           league=current_league.title(),
                           standings=current_standings,
                           table_id=table_id,
                           logo=logo,
                           page='all_games'
                           )


def set_league_info(current_league):
    league = f"{WEBSITE_URL}{leagues[current_league]}"
    table_id = league_ids[current_league]
    logo = league_logos[current_league]

    return league, table_id, logo


def reset_and_get_new_league_values(league):
    """
    Function to reset all of the lists and dictionary values in preparation for new league values being populated

    :param league:
    :return:
    """
    reset_all_value_stores()
    get_games_played(f"{league}-results/")
    get_fixtures(f"{league}-fixtures/")
    get_current_standings(f"{league}-table/")
    convert_data()

    total_goals_scored_dict = merge_dict(home_goals_scored_dict, away_goals_scored_dict)
    total_goals_conceded_dict = merge_dict(home_goals_conceded_dict, away_goals_conceded_dict)
    all_results_dict = merge_dict(away_team_results_dict, home_team_results_dict)

    results = get_suggested_matches(total_goals_scored_dict, total_goals_conceded_dict, all_results_dict)

    return results


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
