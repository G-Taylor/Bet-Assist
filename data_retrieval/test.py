from data_retrieval.game_fixtures_and_results import *
from data_retrieval.runner import get_league

total_goals_scored_dict = {}
total_goals_conceded_dict = {}
all_results_dict = {}
CHOICE = get_league()

get_games_played(CHOICE + 'results/')
get_fixtures(CHOICE + 'fixtures/')
convert_data()


def convert_stats():
    # merging dictionaries together so team name has goals scored/conceded/results beside for future use
    total_goals_scored_dict = merge_dict(home_goals_scored_dict, away_goals_scored_dict)
    total_goals_conceded_dict = merge_dict(home_goals_conceded_dict, away_goals_conceded_dict)
    all_results_dict = merge_dict(away_team_results_dict, home_team_results_dict)

