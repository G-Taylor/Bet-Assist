from .get_total_goals import GetTotalGoals as totalGoals


class GetAverageGoals:
    def __init__(self):
        pass

    @staticmethod
    def get_average_goals(goal_dict) -> float:
        """
        Function that returns the average goals for a team, based on home and away goals
        :param goal_dict:
        :return: avg_goals
        """
        for team in goal_dict:
            total_goals = totalGoals.get_total_goals(team, goal_dict)
            avg_goals = total_goals / len(goal_dict)
            return avg_goals
