class CheckBothTeamsToScore:
    def __init__(self):
        pass

    @staticmethod
    def check_btts(matches):
        """
        Function to set the BTTS boolean value for each match, based on the predefined rules

        :param matches:
        :return: updated matches dictionary, with boolean value for btts
        """
        for match in matches:
            if matches[match]['home_goals_scored'] >= 1.2 and matches[match]['home_goals_conceded'] >= 1:
                if matches[match]['away_goals_scored'] >= 1.2 and matches[match]['away_goals_conceded'] >= 1:
                    matches[match]['btts'] = True

            if matches[match]['match_btts_rating'] >= 70:
                matches[match]['btts'] = True
        return matches

    @staticmethod
    def get_btts_rating(home_goals_scored, home_goals_conceded, away_goals_scored, away_goals_conceded):
        """
        Function that checks all of a games previous matches to see if both teams scored in each match, and returns the
        total percentage of those matches that were btts.

        :param home_goals_scored:
        :param home_goals_conceded:
        :param away_goals_scored:
        :param away_goals_conceded:
        :return: float btts rating for each team in the specified league
        """
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
                print(f'Error in btts home_goals_scored: {e}')

            try:
                if len(away_goals_scored.get(team)) is not None:
                    for i in range(len(away_goals_scored.get(team))):
                        if away_goals_scored[team][i] > 0 and away_goals_conceded[team][i] > 0:
                            btts += 1
                        number_of_matches += 1
            except TypeError as e:
                print(f'Error in btts away_goals_scored: {e}')

            percentage_rating = int((btts/number_of_matches) * 100)
            btts_rating[team] = percentage_rating
        return btts_rating

    @staticmethod
    def assign_btts_ratings(matches, btts_rating):
        """
        Function that assigns the btts rating for each team into the matches dictionary

        :param matches: dictionary containing all match details
        :param btts_rating: float value showing the percentage of games that were btts for a team
        :return: updated matches dictionary containing btts_rating for home team, away team and match average
        """
        for match in matches:
            home_team_rating = btts_rating.get(matches[match]['home_team'])
            away_team_rating = btts_rating.get(matches[match]['away_team'])
            match_btts_rating = (home_team_rating + away_team_rating) // 2

            matches[match]['home_team_btts_rating'] = home_team_rating
            matches[match]['away_team_btts_rating'] = away_team_rating
            matches[match]['match_btts_rating'] = match_btts_rating
        return matches
