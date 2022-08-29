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
        # for match in matches:
        #     if (matches[match]['home_goals_scored'] > '1.5' and matches[match]['home_goals_conceded'] > '0.8') \
        #             and (matches[match]['away_goals_scored'] > '1.5' and matches[match]['away_goals_conceded'] > '0.8'):
        #         matches[match]['btts'] = True
        # return matches

        for match in matches:
            if (matches[match]['home_goals_scored'] > '1.5' and matches[match]['home_goals_conceded'] > '0.8') \
                                and (matches[match]['away_goals_scored'] > '1.5' and matches[match]['away_goals_conceded'] > '0.8'):
                if matches[match]['match_btts_rating'] >= 80:
                    matches[match]['btts'] = True
        return matches

    @staticmethod
    def get_btts_rating(home_goals_scored, home_goals_conceded, away_goals_scored, away_goals_conceded):
        btts_rating = {}
        league_team_keys = []
        [league_team_keys.append(team) for team in home_goals_scored.keys()]
        [league_team_keys.append(team) for team in away_goals_scored.keys() if team not in league_team_keys]

        for team in league_team_keys:
            number_of_matches = 0
            btts = 0
            try:
                for i in range(len(home_goals_scored.get(team))):
                    if home_goals_scored[team][i] > 0 and home_goals_conceded[team][i] > 0:
                        btts += 1
                    number_of_matches += 1
            except TypeError as e:
                print(e)

            try:
                if len(away_goals_scored.get(team)) is not None:
                    for i in range(len(away_goals_scored.get(team))):
                        if away_goals_scored[team][i] > 0 and away_goals_conceded[team][i] > 0:
                            btts += 1
                        number_of_matches += 1
            except TypeError as e:
                print(e)

            percentage_rating = int((btts/number_of_matches) * 100)
            btts_rating[team] = percentage_rating

        return btts_rating

    @staticmethod
    def assign_btts_ratings(matches, btts_rating):
        for match in matches:
            home_team_rating = btts_rating.get(matches[match]['home_team'])
            away_team_rating = btts_rating.get(matches[match]['away_team'])
            match_btts_rating = (home_team_rating + away_team_rating) // 2

            matches[match]['home_team_btts_rating'] = home_team_rating
            matches[match]['away_team_btts_rating'] = away_team_rating
            matches[match]['match_btts_rating'] = match_btts_rating

        return matches
