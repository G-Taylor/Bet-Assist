from flask import Flask, render_template, jsonify
from utilities.merge_two_dicts import MergeDict
from config import initialise_cache
from utilities.get_dictionary_length import GetDictionaryLength
from data_retrieval.Main import get_suggested_matches
from data_retrieval.game_fixtures_and_results import *
from league_info.league_metadata import leagues, WEBSITE_URL


app = Flask(__name__)
cache = initialise_cache(app)


# App Route for the index page of the application
@app.route('/', methods=['GET', 'POST'])
@cache.cached(timeout=50)
def index():
    return render_template('index.html')


# App Route for the Over 2.5 goals games page of the application
@app.route('/over2/<cl>', methods=['GET', 'POST'])
@cache.cached(timeout=50)
def over2(cl):
    try:
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
    except KeyError:
        league = cl

        return render_template(
            'error.html',
            league=league,
            page='over2'
        )

# App Route for the Both Teams To Score games page of the application
@app.route('/btts/<cl>', methods=['GET', 'POST'])
@cache.cached(timeout=50)
def btts(cl):
    try:
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
    except KeyError:
        league = cl

        return render_template(
            'error.html',
            league=league,
            page='btts'
        )


# App Route for the all games page of the application
@app.route('/all_games/<cl>', methods=['GET', 'POST'])
@cache.cached(timeout=900)
def all_games(cl):
    try:
        current_league = cl
        league, table_id, logo = set_league_info(current_league)

        results = reset_and_get_new_league_values(league)

        return render_template(
            'all_games.html',
            res=results,
            league=current_league.title(),
            standings=current_standings,
            table_id=table_id,
            logo=logo,
            page='all_games'
        )
    except KeyError:
        league = cl

        return render_template(
            'error.html',
            league=league,
            page='all_games'
        )


# API endpoint for all games function
@app.route('/api/all_games/<cl>', methods=['GET'])
@cache.cached(timeout=900)
def all_games_api(cl):
    current_league = cl
    league, table_id, logo = set_league_info(current_league)

    results = reset_and_get_new_league_values(league)

    return jsonify(
        results=results,
        league=current_league.title(),
        standings=current_standings,
        table_id=table_id,
        logo=logo,
        page='all_games',
    )


def set_league_info(current_league):
    league = f"{WEBSITE_URL}{leagues[current_league]['url']}"
    table_id = leagues[current_league]['id']
    logo = leagues[current_league]['logo']
    return league, table_id, logo


def reset_and_get_new_league_values(league):
    """
    Function to reset all of the lists and dictionary values in preparation for new league values being populated

    :param league:
    :return:
    """
    reset_all_value_stores()
    get_games_played(f"{league}-results/")
    fixture_scrape_data = get_fixtures(f"{league}-fixtures/")
    convert_data()

    total_goals_scored_dict = MergeDict.merge_dicts(home_goals_scored_dict, away_goals_scored_dict)
    total_goals_conceded_dict = MergeDict.merge_dicts(home_goals_conceded_dict, away_goals_conceded_dict)
    all_results_dict = MergeDict.merge_dicts(away_team_results_dict, home_team_results_dict)

    results = get_suggested_matches(total_goals_scored_dict,
                                    total_goals_conceded_dict,
                                    all_results_dict,
                                    fixture_scrape_data,
                                    GetDictionaryLength)

    return results


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
