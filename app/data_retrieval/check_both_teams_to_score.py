class CheckBothTeamsToScore:
    def __init__(self):
        pass

    @staticmethod
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
