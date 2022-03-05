from data_retrieval.game_stats_retrieval import get_total_goals, get_dict_length
# from data_retrieval.test import *
from data_retrieval.game_fixtures_and_results import *

teams_over_2_goals = {}
teams_over_2_goals_scored = {}
teams_over_2_goals_conceded = {}
# teams_over_4_wins = get_last_results('won')
# teams_over_4_losses = get_last_results('lost')
# teams_over_4_draws = get_last_results('draw')


def get_teams_over_2(total_goals_scored_dict, total_goals_conceded_dict):
    for team in total_goals_scored_dict:
        # print(team, total_goals_conceded_dict[team])
        # if((get_total_goals(team, total_goals_conceded_dict) / 5) >= 1.2):
        #     if((get_total_goals(team, total_goals_scored_dict) / 5) >= 1.2):
        #         teams_over_2_goals.append(team)
        #         print(team)
        if (get_total_goals(team, total_goals_scored_dict) / 5) >= 2:
            teams_over_2_goals.append(team)
            # print(team)
            continue

        if (get_total_goals(team, total_goals_conceded_dict) / 5) >= 1.2:
            teams_over_2_goals.append(team)
            # print(team)
            continue


def get_teams_over_2_point_5_new(total_goals_scored_dict, total_goals_conceded_dict):
    for team in total_goals_scored_dict:
        total_goals = get_total_goals(team, total_goals_scored_dict) + get_total_goals(team, total_goals_conceded_dict)
        games_played = get_dict_length(team, total_goals_scored_dict)
        avg_goals = total_goals / games_played
        avg_goals_scored = get_total_goals(team, total_goals_scored_dict) / games_played
        avg_goals_conceded = get_total_goals(team, total_goals_conceded_dict) / games_played

        if avg_goals >= 2.5:
            # print(team, avg_goals)
            teams_over_2_goals[team] = avg_goals
            teams_over_2_goals_scored[team] = avg_goals_scored
            teams_over_2_goals_conceded[team] = avg_goals_conceded

    # print(teams_over_2_goals)
            # teams_over_2_goals.append(team, avg_goals)


def get_teams_over_2_point_5(total_goals_scored_dict, total_goals_conceded_dict):
    for team in total_goals_scored_dict:
        total_goals = get_total_goals(team, total_goals_scored_dict) + get_total_goals(team, total_goals_conceded_dict)
        games_played = get_dict_length(team, total_goals_scored_dict)
        avg_goals = total_goals / games_played

        if avg_goals >= 2.5:
            # print(team, avg_goals)
            teams_over_2_goals[team] = avg_goals

    # print(teams_over_2_goals)
            # teams_over_2_goals.append(team, avg_goals)


# def get_home_teams_to_win():
#     print('\n', '*' * 11, ' Home Teams to Win ', '*' * 11)
#     for team in teams_over_4_wins:
#         home_index = home_fixture_list.index(team)
#         away_index = 0
#         for team2 in teams_over_4_losses:
#             away_index = away_fixture_list.index(team2)
#             if home_index == away_index:
#                 print('\t', team, ' vs ', team2)


# def get_away_teams_to_win():
#     print('\n', '*' * 11, ' Away Teams to Win ', '*' * 11)
#     for team in teams_over_4_wins:
#         away_index = away_fixture_list.index(team)
#         home_index = 0
#         for team2 in teams_over_4_losses:
#             home_index = home_fixture_list.index(team2)
#             if away_index == home_index:
#                 print('\t', team2, ' vs ', team)


# def get_home_teams_to_draw():
#     print('\n', '*' * 11, ' Teams to Draw ', '*' * 11)
#     for team in teams_over_4_draws:
#         home_index = home_fixture_list.index(team)
#         away_index = 0
#         for team2 in teams_over_4_draws:
#             away_index = away_fixture_list.index(team2)
#             if home_index == away_index:
#                 print('\t', team, ' vs ', team2)


def get_fixture_over_2(total_goals_scored_dict, total_goals_conceded_dict, all_results_dict):
    suggested_matches = {}
    get_teams_over_2_point_5_new(total_goals_scored_dict, total_goals_conceded_dict)
    print('', '*' * 30, ' Over 2.5 Goals ', '*' * 30)
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

                    print('\t', f'{all_results_dict[team]}\t\t', f'{teams_over_2_goals[team]:.2f}', team, ' vs ',
                          team2, f'{teams_over_2_goals[team2]:.2f}', f'\t\t{all_results_dict[team2]}')
                    print('\t\t\t\t\t', f'Goals Scored:\t\t\t{teams_over_2_goals_scored[team]:.2f}\t\t\t', f'{teams_over_2_goals_scored[team2]:.2f}')
                    print('\t\t\t\t\t', f'Goals Conceded:\t\t{teams_over_2_goals_conceded[team]:.2f}\t\t\t', f'{teams_over_2_goals_conceded[team2]:.2f}\n')
        except ValueError:
            pass

    return suggested_matches
# get_fixture_over_2()


