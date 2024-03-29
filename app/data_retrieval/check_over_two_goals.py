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
            
            over2_result = 0

            if 1 <= matches[match]['home_goals_scored'] < 2:
                over2_result += 1
            elif 2 <= matches[match]['home_goals_scored'] < 3:
                over2_result += 2
            elif matches[match]['home_goals_scored'] >= 3:
                over2_result += 3

            if .5 <= matches[match]['home_goals_conceded'] < 1:
                over2_result += 1
            elif 1 <= matches[match]['home_goals_conceded'] < 2:
                over2_result += 2
            elif matches[match]['home_goals_conceded'] >= 2:
                over2_result += 3

            if 1.5 <= matches[match]['home_average_goals'] < 2.5:
                over2_result += 1
            elif 2.5 <= matches[match]['home_average_goals'] < 3.5:
                over2_result += 2
            elif matches[match]['home_average_goals'] >= 3.5:
                over2_result += 3

            if 1 <= matches[match]['away_goals_scored'] < 2:
                over2_result += 1
            elif 2 <= matches[match]['away_goals_scored'] < 3:
                over2_result += 2
            elif matches[match]['away_goals_scored'] >= 3:
                over2_result += 3

            if .5 <= matches[match]['away_goals_conceded'] < 1:
                over2_result += 1
            elif 1 <= matches[match]['away_goals_conceded'] < 2:
                over2_result += 2
            elif matches[match]['away_goals_conceded'] >= 2:
                over2_result += 3

            if 1.5 <= matches[match]['away_average_goals'] < 2.5:
                over2_result += 1
            elif 2.5 <= matches[match]['away_average_goals'] < 3.5:
                over2_result += 2
            elif matches[match]['away_average_goals'] >= 3.5:
                over2_result += 3

            if 1.5 <= matches[match]['total_average_goals'] < 2.5:
                over2_result += 1
            elif 2.5 <= matches[match]['total_average_goals'] < 3.5:
                over2_result += 2
            elif matches[match]['total_average_goals'] >= 3.5:
                over2_result += 3

            if matches[match]['home_team_over2_rating'] == 100:
                over2_result += 5
            elif 60 <= matches[match]['home_team_over2_rating'] < 70:
                over2_result += 1
            elif 70 <= matches[match]['home_team_over2_rating'] < 80:
                over2_result += 2
            elif matches[match]['home_team_over2_rating'] >= 80:
                over2_result += 3

            if matches[match]['away_team_over2_rating'] == 100:
                over2_result += 5
            elif 60 <= matches[match]['away_team_over2_rating'] < 70:
                over2_result += 1
            elif 70 <= matches[match]['away_team_over2_rating'] < 80:
                over2_result += 2
            elif matches[match]['away_team_over2_rating'] >= 80:
                over2_result += 3

            if matches[match]['match_over2_rating'] == 100:
                over2_result += 5
            if 60 <= matches[match]['match_over2_rating'] < 70:
                over2_result += 1
            elif 70 <= matches[match]['match_over2_rating'] < 80:
                over2_result += 2
            elif matches[match]['match_over2_rating'] >= 80:
                over2_result += 3
            
            over2_result = (over2_result/30)*100

            if over2_result >= 70:
                matches[match]['over2.5'] = True
            
            matches[match]['over2_calculated_score'] = int(over2_result)
        return matches

    @staticmethod
    def get_over2_rating(home_goals_scored, home_goals_conceded, away_goals_scored, away_goals_conceded):
        over2_rating = {}
        league_team_keys = []
        [league_team_keys.append(team) for team in home_goals_scored.keys()]
        [league_team_keys.append(team) for team in away_goals_scored.keys() if team not in league_team_keys]

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
