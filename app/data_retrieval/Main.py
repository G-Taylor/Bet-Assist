from .game_fixtures_and_results import *
from .game_stats_retrieval import get_total_goals, get_dict_length

teams_over_2_goals = {}
teams_over_2_goals_scored = {}
teams_over_2_goals_conceded = {}


def get_teams_over_2_point_5_new(total_goals_scored_dict, total_goals_conceded_dict):
    """
    Old function to get the teams that have an average goal count >= 2.5
    or have an average goals scored total >= 3 from their last matches

    :param total_goals_scored_dict:
    :param total_goals_conceded_dict:
    :return:
    """
    for team in total_goals_scored_dict:
        total_goals = get_total_goals(team, total_goals_scored_dict) + get_total_goals(team, total_goals_conceded_dict)
        games_played = get_dict_length(team, total_goals_scored_dict)
        avg_goals = total_goals / games_played
        avg_goals_scored = get_total_goals(team, total_goals_scored_dict) / games_played
        avg_goals_conceded = get_total_goals(team, total_goals_conceded_dict) / games_played

        if avg_goals >= 2.5 or avg_goals_scored >= 3:
            teams_over_2_goals[team] = avg_goals
            teams_over_2_goals_scored[team] = avg_goals_scored
            teams_over_2_goals_conceded[team] = avg_goals_conceded


def get_all_fixtures(total_goals_scored_dict, total_goals_conceded_dict):
    """
    Gets all of the goal info for the upcoming fixtures

    :param total_goals_scored_dict:
    :param total_goals_conceded_dict:
    :return:
    """
    for team in total_goals_scored_dict:
        total_goals = get_total_goals(team, total_goals_scored_dict) + get_total_goals(team, total_goals_conceded_dict)
        games_played = get_dict_length(team, total_goals_scored_dict)
        avg_goals = total_goals / games_played
        avg_goals_scored = get_total_goals(team, total_goals_scored_dict) / games_played
        avg_goals_conceded = get_total_goals(team, total_goals_conceded_dict) / games_played

        teams_over_2_goals[team] = avg_goals
        teams_over_2_goals_scored[team] = avg_goals_scored
        teams_over_2_goals_conceded[team] = avg_goals_conceded


def get_suggested_matches(league, total_goals_scored_dict, total_goals_conceded_dict, all_results_dict, fixture_scrape_data):
    """
    Function that gets key details for each team and adds it to a dictionary 'suggested_matches'

    :param fixture_scrape_data:
    :param league:
    :param total_goals_scored_dict: a dictionary containing all of the goals a team has scored in each match
    :param total_goals_conceded_dict: a dictionary containing all of the goals a team has conceded in each match
    :param all_results_dict: a dictionary containing win/lost/draw results for each team
    :return suggested_matches: a dictionary containing upcoming matches and the important information associated with them
    """
    suggested_matches = {}
    get_all_fixtures(total_goals_scored_dict, total_goals_conceded_dict)

    for team in teams_over_2_goals:
        try:
            home_index = home_fixture_list.index(team)
            for team2 in teams_over_2_goals:
                if team2 in away_fixture_list[::-1]:
                    away_index = away_fixture_list.index(team2)
                    if home_index == away_index:
                        date, time = get_date_and_time(fixture_scrape_data, team, team2)
                        suggested_matches[home_index] = {}
                        suggested_matches[home_index]['date'] = date
                        suggested_matches[home_index]['time'] = time
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
                        suggested_matches[home_index]['total_average_goals'] = f'{(teams_over_2_goals[team] + teams_over_2_goals[team2]) /2:.2f}'
                        suggested_matches[home_index]['btts'] = False
                        suggested_matches[home_index]['over2.5'] = False
        except ValueError:
            pass

    teams_over_2_goals.clear()
    teams_over_2_goals_scored.clear()
    teams_over_2_goals_conceded.clear()

    check_btts(suggested_matches)
    check_over2(suggested_matches)
    return suggested_matches


def check_btts(matches):
    """
    Function to set the BTTS boolean value for each match, based on predefined rules

    :param matches:
    :return:
    """
    for match in matches:
        if (matches[match]['home_goals_scored'] > '1.5' and matches[match]['home_goals_conceded'] > '0.8') \
                and (matches[match]['away_goals_scored'] > '1.5' and matches[match]['away_goals_conceded'] > '0.8'):
            matches[match]['btts'] = True
    return matches


def check_over2(matches):
    """
    Function to set the Over 2.5 boolean value for each match, based on predefined rules

    :param matches:
    :return:
    """
    for match in matches:
        if matches[match]['total_average_goals'] > '3.25':
            matches[match]['over2.5'] = True
    return matches
