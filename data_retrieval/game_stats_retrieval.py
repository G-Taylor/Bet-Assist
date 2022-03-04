# from data_retrieval.test import all_results_dict


# def get_last_results(result):
#     team_list = []
#
#     for team in all_results_dict:
#         result_list = []
#         result_list += all_results_dict[team][0]
#         result_list += all_results_dict[team][1]
#         # total_results = result_list + result_list2
#
#         if result == 'won' and result_list.count('W') >= 4:
#             team_list.append(team)
#         elif result == 'lost' and result_list.count('L') >= 3:
#             team_list.append(team)
#         elif result == 'draw' and result_list.count('D') >= 3:
#             team_list.append(team)
#
#     return team_list


def get_total_goals(team_name, goal_dict):
    try:
        goals = sum(goal_dict[team_name][1])
    except:
        goals = sum(goal_dict[team_name])
        return goals
    else:
        goals += sum(goal_dict[team_name][0])
        return goals


def get_dict_length(team_name, goal_dict):
    try:
        length = len(goal_dict[team_name][1])
    except:
        length = len(goal_dict[team_name])
        return length
    else:
        length += len(goal_dict[team_name][0])
        return length


def get_average_goals(goal_dict):
    for team in goal_dict:
        total_goals = get_total_goals(team, goal_dict)
        avg_goals = total_goals / len(goal_dict)
        return avg_goals