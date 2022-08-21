class CheckOverTwoGoals:
    def __init__(self):
        pass

    @staticmethod
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
