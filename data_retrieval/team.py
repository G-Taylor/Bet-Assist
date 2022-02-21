from requests import get
from bs4 import BeautifulSoup


class Team:
    def __init__(self, name):
        self.name = name
        self.league = ''
        self.scored = []
        self.conceded = []
        self.results = []

    def get_name(self):
        return self.name

    def get_league(self):
        return self.league

    def get_goals_scored(self):
        return self.scored

    def get_goals_conceded(self):
        return self.conceded

    def get_results(self):
        return self.results

    def get_total_goals(self):
        return self.scored + self.conceded

    def get_avg_goals(self):
        return self.get_total_goals() / len(self.results)

    def __str__(self):
        return 'Team: {}\nLeague: {}\nResults: {}'.format(self.name, self.league, self.results)