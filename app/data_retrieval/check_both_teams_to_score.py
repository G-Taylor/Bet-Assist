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

    @staticmethod
    def get_btts_rating(matches, home_goals_scored, home_goals_conceded, away_goals_scored, away_goals_conceded):
        # print(f'{matches[match]["home_team"]} Scored: {home_goals_scored[matches[match]["home_team"]]} ')
        # print(f'{matches[match]["home_team"]} Conceded: {home_goals_conceded[matches[match]["home_team"]]} ')

        for team in home_goals_scored.keys():
            number_of_matches = 0.0
            btts = 0.0

            for i in range(len(home_goals_scored.get(team))):
                if home_goals_scored[team][i] > 0 and home_goals_conceded[team][i] > 0:
                    print(f'{team} BTTS: {True}')
                    btts += 1
                    number_of_matches += 1
                else:
                    print(f'{team} BTTS: {False}')
                    number_of_matches += 1
            print(f'{team}: {home_goals_scored.get(team)}')
            print(f'{team}: {home_goals_conceded.get(team)}')

            for i in range(len(away_goals_scored.get(team))):
                if away_goals_scored[team][i] > 0 and away_goals_conceded[team][i] > 0:
                    print(f'{team} BTTS: {True}')
                    btts += 1
                    number_of_matches += 1
                else:
                    print(f'{team} BTTS: {False}')
                    number_of_matches += 1
            print(f'{team}: {away_goals_scored.get(team)}')
            print(f'{team}: {away_goals_conceded.get(team)}')
            print(f'BTTS: {btts}')
            print(f'Matches: {number_of_matches}')
            print(f'{btts/number_of_matches}')

