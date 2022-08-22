class GetTotalGoals:
    def __init__(self):
        pass

    @staticmethod
    def get_total_goals(team_name, goal_dict):
        try:
            goals = sum(goal_dict[team_name][1])
        except:
            goals = sum(goal_dict[team_name])
            return goals
        else:
            goals += sum(goal_dict[team_name][0])
            return goals
