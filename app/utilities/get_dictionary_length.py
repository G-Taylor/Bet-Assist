class GetDictionaryLength:
    def __init__(self):
        pass

    @staticmethod
    def get_dict_length(team_name, goal_dict):
        """
        Gets the length of the dictionary. Each dictionary can possibly contain tuples, so try catch block accounts for that

        :param team_name:
        :param goal_dict:
        :return:
        """
        try:
            length = len(goal_dict[team_name][1])
        except:
            length = len(goal_dict[team_name])
            return length
        else:
            length += len(goal_dict[team_name][0])
            return length
