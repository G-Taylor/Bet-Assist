from flask import Flask, render_template, request, url_for
from data_retrieval.Main import get_fixture_over_2, teams_over_2_goals, teams_over_2_goals_scored, teams_over_2_goals_conceded
from data_retrieval.game_fixtures_and_results import *
from data_retrieval.league_urls import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    current_league = "Premiership"
    league = f"{WEBSITE_URL}{leagues[current_league]}"

    if request.method == "POST":
        current_league = request.form.get('league')
        league = f"{WEBSITE_URL}{leagues[current_league]}"

    reset_all_value_stores()
    get_games_played(f"{league}results/")
    get_fixtures(f"{league}fixtures/")
    # get_standings(f"{league}standings/")
    convert_data()

    total_goals_scored_dict = merge_dict(home_goals_scored_dict, away_goals_scored_dict)
    total_goals_conceded_dict = merge_dict(home_goals_conceded_dict, away_goals_conceded_dict)
    all_results_dict = merge_dict(away_team_results_dict, home_team_results_dict)

    results = get_fixture_over_2(total_goals_scored_dict, total_goals_conceded_dict, all_results_dict)

    return render_template('index.html',
                           results=results,
                           current_league=current_league
                           )


if __name__ == '__main__':
    app.run(debug=True)
