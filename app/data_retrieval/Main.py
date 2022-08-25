from .game_fixtures_and_results import *
from .get_match_date_and_time import GetMatchDateAndTime
from .check_both_teams_to_score import CheckBothTeamsToScore
from .check_over_two_goals import CheckOverTwoGoals
from .get_total_goals import GetTotalGoals as totalGoals
from collections import OrderedDict

teams_over_2_goals = {}
teams_over_2_goals_scored = {}
teams_over_2_goals_conceded = {}


def get_all_fixtures(total_goals_scored_dict, total_goals_conceded_dict, dictionary_length):
    """
    Gets all of the goal info for the upcoming fixtures

    :param dictionary_length:
    :param total_goals_scored_dict:
    :param total_goals_conceded_dict:
    :return:
    """
    for team in total_goals_scored_dict:
        total_goals = totalGoals.get_total_goals(team, total_goals_scored_dict) + totalGoals.get_total_goals(team, total_goals_conceded_dict)
        games_played = dictionary_length.get_dict_length(team, total_goals_scored_dict)
        avg_goals = total_goals / games_played
        avg_goals_scored = totalGoals.get_total_goals(team, total_goals_scored_dict) / games_played
        avg_goals_conceded = totalGoals.get_total_goals(team, total_goals_conceded_dict) / games_played

        teams_over_2_goals[team] = avg_goals
        teams_over_2_goals_scored[team] = avg_goals_scored
        teams_over_2_goals_conceded[team] = avg_goals_conceded


def get_suggested_matches(total_goals_scored_dict,
                          total_goals_conceded_dict,
                          all_results_dict,
                          fixture_scrape_data,
                          dictionary_length
                          ):
    """
    Function that gets key details for each team and adds it to a dictionary 'suggested_matches'

    :param dictionary_length:
    :param fixture_scrape_data:
    :param total_goals_scored_dict: a dictionary containing all of the goals a team has scored in each match
    :param total_goals_conceded_dict: a dictionary containing all of the goals a team has conceded in each match
    :param all_results_dict: a dictionary containing win/lost/draw results for each team
    :return suggested_matches: a dictionary containing upcoming matches and
            the important information associated with them
    """
    suggested_matches = {}
    get_all_fixtures(total_goals_scored_dict, total_goals_conceded_dict, dictionary_length)

    for team in teams_over_2_goals:
        try:
            home_index = home_fixture_list.index(team)
            for team2 in teams_over_2_goals:
                if team2 in away_fixture_list[::-1]:
                    away_index = away_fixture_list.index(team2)
                    if home_index == away_index:
                        fixture = f'{team} vs {team2}'
                        suggested_matches[fixture] = {}

                        try:
                            date, time, parsed_date = GetMatchDateAndTime\
                                .get_date_and_time(fixture_scrape_data, team, team2)
                            suggested_matches[fixture]['date'] = date
                            suggested_matches[fixture]['time'] = time
                            suggested_matches[fixture]['parsed_date'] = parsed_date
                        except TypeError as e:
                            print(f'Error getting date/time - {e}')
                            suggested_matches[fixture]['date'] = ''
                            suggested_matches[fixture]['time'] = ''
                            suggested_matches[fixture]['parsed_date'] = ''

                        suggested_matches[fixture]['home_team'] = team
                        suggested_matches[fixture]['home_results'] = all_results_dict[team]
                        suggested_matches[fixture]['home_average_goals'] = f'{teams_over_2_goals[team]:.2f}'
                        suggested_matches[fixture]['home_goals_scored'] = f'{teams_over_2_goals_scored[team]:.2f}'
                        suggested_matches[fixture]['home_goals_conceded'] = f'{teams_over_2_goals_conceded[team]:.2f}'
                        suggested_matches[fixture]['home_team_btts_rating'] = 0
                        suggested_matches[fixture]['home_team_over2_rating'] = 0

                        suggested_matches[fixture]['away_team'] = team2
                        suggested_matches[fixture]['away_results'] = all_results_dict[team2]
                        suggested_matches[fixture]['away_average_goals'] = f'{teams_over_2_goals[team2]:.2f}'
                        suggested_matches[fixture]['away_goals_scored'] = f'{teams_over_2_goals_scored[team2]:.2f}'
                        suggested_matches[fixture]['away_goals_conceded'] = f'{teams_over_2_goals_conceded[team2]:.2f}'
                        suggested_matches[fixture]['away_team_btts_rating'] = 0
                        suggested_matches[fixture]['away_team_over2_rating'] = 0

                        suggested_matches[fixture]['total_average_goals'] = \
                            f'{(teams_over_2_goals[team] + teams_over_2_goals[team2]) /2:.2f}'
                        suggested_matches[fixture]['match_btts_rating'] = 0
                        suggested_matches[fixture]['match_over2_rating'] = 0
                        suggested_matches[fixture]['over2.5'] = False
                        suggested_matches[fixture]['btts'] = False
        except ValueError:
            pass

    teams_over_2_goals.clear()
    teams_over_2_goals_scored.clear()
    teams_over_2_goals_conceded.clear()

    btts_ratings = CheckBothTeamsToScore.get_btts_rating(home_goals_scored_dict,
                                                         home_goals_conceded_dict,
                                                         away_goals_scored_dict,
                                                         away_goals_conceded_dict
                                                         )

    over2_ratings = CheckOverTwoGoals.get_over2_rating(home_goals_scored_dict,
                                                       home_goals_conceded_dict,
                                                       away_goals_scored_dict,
                                                       away_goals_conceded_dict
                                                       )

    CheckBothTeamsToScore.assign_btts_ratings(suggested_matches, btts_ratings)
    CheckBothTeamsToScore.check_btts(suggested_matches)
    CheckOverTwoGoals.assign_over2_ratings(suggested_matches, over2_ratings)
    CheckOverTwoGoals.check_over2(suggested_matches)
    suggested_matches = OrderedDict(sorted(suggested_matches.items(), key=lambda x: str(x[1]['parsed_date'])))
    return suggested_matches
