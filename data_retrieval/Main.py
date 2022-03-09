from data_retrieval.game_fixtures_and_results import *
from data_retrieval.game_stats_retrieval import get_total_goals, get_dict_length

teams_over_2_goals = {}
teams_over_2_goals_scored = {}
teams_over_2_goals_conceded = {}


def get_teams_over_2_point_5_new(total_goals_scored_dict, total_goals_conceded_dict):
    for team in total_goals_scored_dict:
        total_goals = get_total_goals(team, total_goals_scored_dict) + get_total_goals(team, total_goals_conceded_dict)
        games_played = get_dict_length(team, total_goals_scored_dict)
        avg_goals = total_goals / games_played
        avg_goals_scored = get_total_goals(team, total_goals_scored_dict) / games_played
        avg_goals_conceded = get_total_goals(team, total_goals_conceded_dict) / games_played

        if avg_goals >= 2.5:
            teams_over_2_goals[team] = avg_goals
            teams_over_2_goals_scored[team] = avg_goals_scored
            teams_over_2_goals_conceded[team] = avg_goals_conceded


# Returns the expected matches to be over 2.5 goals or btts
def get_fixture_over_2(total_goals_scored_dict, total_goals_conceded_dict, all_results_dict):
    suggested_matches = {}
    get_teams_over_2_point_5_new(total_goals_scored_dict, total_goals_conceded_dict)

    for team in teams_over_2_goals:
        try:
            home_index = home_fixture_list.index(team)
            away_index = 0
            for team2 in teams_over_2_goals:
                away_index = away_fixture_list.index(team2)
                if home_index == away_index:
                    suggested_matches[home_index] = {}
                    suggested_matches[home_index]['home_team'] = team
                    suggested_matches[home_index]['home_results'] = all_results_dict[team]
                    suggested_matches[home_index]['home_average_goals'] = f'{teams_over_2_goals[team]:.2f}'
                    suggested_matches[home_index]['home_goals_scored'] = f'{teams_over_2_goals_scored[team]:.2f}'
                    suggested_matches[home_index]['home_goals_conceded'] = f'{teams_over_2_goals_conceded[team]:.2f}'

                    suggested_matches[home_index]['away_team'] = team2
                    suggested_matches[home_index]['away_results'] = all_results_dict[team2]
                    suggested_matches[home_index]['away_average_goals'] = f'{teams_over_2_goals[team2]:.2f}'
                    suggested_matches[home_index]['away_goals_scored'] = f'{teams_over_2_goals_scored[team2]:.2f}'
                    suggested_matches[home_index]['away_goals_conceded'] = f'{teams_over_2_goals_conceded[team2]:.2f}'
        except ValueError:
            pass

    teams_over_2_goals.clear()
    teams_over_2_goals_scored.clear()
    teams_over_2_goals_conceded.clear()
    return suggested_matches


