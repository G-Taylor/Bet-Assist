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


def get_average_goals(goal_dict) -> float:
    """
    Function that returns the average goals for a team, based on home and away goals
    :param goal_dict:
    :return: avg_goals
    """
    for team in goal_dict:
        total_goals = get_total_goals(team, goal_dict)
        avg_goals = total_goals / len(goal_dict)
        return avg_goals
