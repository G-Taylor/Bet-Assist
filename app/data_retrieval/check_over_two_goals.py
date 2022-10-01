class CheckOverTwoGoals:
    def __init__(self):
        pass

    @staticmethod
    def check_over2(matches):
        """
        Function to set the Over 2.5 boolean value for each match, based on the predefined rules

        :param matches:
        :return:
        """
        # TODO: Update algorithm to provide better/more comprehensive results

        for match in matches:
            # if matches[match]['match_over2_rating'] >= 75:
            #     if matches[match]['total_average_goals'] >= 2.75:
            #         matches[match]['over2.5'] = True

            if matches[match]['match_over2_rating'] >= 75:
                matches[match]['over2.5'] = True

            if matches[match]['match_over2_rating'] < 75 and matches[match]['total_average_goals'] >= 3:
                if matches[match]['home_team_over2_rating'] >= 75:
                    if matches[match]['home_goals_scored'] >= 1.5 and matches[match]['away_goals_conceded'] > 0:
                        matches[match]['over2.5'] = True
        return matches

    @staticmethod
    def get_over2_rating(home_goals_scored, home_goals_conceded, away_goals_scored, away_goals_conceded):
        over2_rating = {}
        league_team_keys = []
        [league_team_keys.append(team) for team in home_goals_scored.keys()]
        [league_team_keys.append(team) for team in away_goals_scored.keys(
        ) if team not in league_team_keys]

        for team in league_team_keys:
            number_of_matches = 0
            over2 = 0
            try:
                for i in range(len(home_goals_scored.get(team))):
                    if (home_goals_scored[team][i] + home_goals_conceded[team][i]) > 2:
                        over2 += 1
                    number_of_matches += 1
            except TypeError as e:
                print(f'Error in over 2.5 home_goals_scored: {e}')

            try:
                if len(away_goals_scored.get(team)) is not None:
                    for i in range(len(away_goals_scored.get(team))):
                        if (away_goals_scored[team][i] + away_goals_conceded[team][i]) > 2:
                            over2 += 1
                        number_of_matches += 1
            except TypeError as e:
                print(f'Error in over 2.5 away_goals_scored: {e}')

            percentage_rating = int((over2 / number_of_matches) * 100)
            over2_rating[team] = percentage_rating

        return over2_rating

    @staticmethod
    def assign_over2_ratings(matches, over2_rating):
        for match in matches:
            home_team_rating = over2_rating.get(matches[match]['home_team'])
            away_team_rating = over2_rating.get(matches[match]['away_team'])
            match_over2_rating = int((home_team_rating + away_team_rating) / 2)

            matches[match]['home_team_over2_rating'] = home_team_rating
            matches[match]['away_team_over2_rating'] = away_team_rating
            matches[match]['match_over2_rating'] = match_over2_rating
        return matches
