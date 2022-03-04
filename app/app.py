from flask import Flask, render_template
from data_retrieval.Main import get_fixture_over_2
from data_retrieval.game_fixtures_and_results import *
from data_retrieval.runner import get_league

app = Flask(__name__)


@app.route('/')
def hello_world():
    league = get_league()
    get_games_played(league + 'results/')
    get_fixtures(league + 'fixtures/')
    convert_data()

    total_goals_scored_dict = merge_dict(home_goals_scored_dict, away_goals_scored_dict)
    total_goals_conceded_dict = merge_dict(home_goals_conceded_dict, away_goals_conceded_dict)
    all_results_dict = merge_dict(away_team_results_dict, home_team_results_dict)

    results = get_fixture_over_2(total_goals_scored_dict, total_goals_conceded_dict, all_results_dict)
    return render_template('index.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
