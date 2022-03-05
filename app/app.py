from flask import Flask, render_template, request
from data_retrieval.Main import get_fixture_over_2
from data_retrieval.game_fixtures_and_results import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    WEBSITE_URL = 'https://www.scorespro.com/soccer/'
    leagues = {
        'Premiership': 'england/premier-league/',
        'Championship': 'england/championship/',
        'League 1': 'england/league-one/',
        'League 2': 'england/league-two/',
        'National League': 'england/national-league/',
        'SCOT': 'scotland/premiership/',
        'La Liga': 'spain/laliga/',
        'Bundesliga': 'germany/bundesliga/',
        'ITALIAN': 'italy/serie-a/',
        'Ligue 1': 'france/ligue-1/',
        'DUTCH': 'netherlands/eredivisie/',
        'CL': 'uefa/champions-league/',
        'EUROPA': 'uefa/europa-league/',
    }

    if request.method == "GET":
        league = f"{WEBSITE_URL}{leagues['Premiership']}"
    else:
        league = f"{WEBSITE_URL}{leagues[request.form.get('league')]}"

    reset_all_values()
    get_games_played(league + 'results/')
    get_fixtures(league + 'fixtures/')
    convert_data()

    total_goals_scored_dict = merge_dict(home_goals_scored_dict, away_goals_scored_dict)
    total_goals_conceded_dict = merge_dict(home_goals_conceded_dict, away_goals_conceded_dict)
    all_results_dict = merge_dict(away_team_results_dict, home_team_results_dict)

    results = get_fixture_over_2(total_goals_scored_dict, total_goals_conceded_dict, all_results_dict)
    return render_template('index.html', results=results)


def reset_all_values():
    home_goals_scored.clear()
    home_goals_scored_dict.clear()
    away_goals_conceded.clear()
    away_goals_scored_dict.clear()
    home_goals_conceded.clear()
    home_goals_conceded_dict.clear()
    away_goals_conceded.clear()
    away_goals_conceded_dict.clear()
    away_team_results.clear()
    away_team_results_dict.clear()
    home_team_results.clear()
    home_team_results_dict.clear()


if __name__ == '__main__':
    app.run(debug=True)
