import os
import requests
from bs4 import BeautifulSoup

# lists and dictionaries used for storing results
home_team_list = []
away_team_list = []

home_goals_scored = []
home_goals_conceded = []
away_goals_scored = []
away_goals_conceded = []

home_team_results = []
away_team_results = []
home_team_results_dict = {}
away_team_results_dict = {}

home_goals_scored_dict = {}
home_goals_conceded_dict = {}
away_goals_scored_dict = {}
away_goals_conceded_dict = {}

total_goals_scored = []
total_goals_conceded = []

# lists ued to store upcoming fixtures
home_fixture_list = []
away_fixture_list = []

# Dictionary for storing the current standings
current_standings = {}


def strip_and_add_team(team, team_list):
    """
    function to scrape the team name from the website, and add it to the team_list

    :param team:
    :param team_list:
    :return:
    """

    if team is not None:
        # team_name = team.find(class_='swap-text__target')
        team_name = team.find(class_=os.environ.get('SS_STRIPPED_TEAM_NAME'))
        team_list.append(team_name.text)


def convert_to_dict(team_list, goal_list, results_dict):
    """
    function to convert any two lists into a dictionary

    :param team_list:
    :param goal_list:
    :param results_dict:
    :return:
    """

    res = [(team_list[i], goal_list[i]) for i in range(0, len(team_list))]
    [results_dict.setdefault(team, []).append(goals) for team, goals in res]


def get_fixtures(league):
    """
    function to scrape upcoming fixtures from source website

    :param league:
    :return:
    """
    all_home_matches = []
    all_away_matches = []

    page = requests.get(league)
    soup = BeautifulSoup(page.content, 'html.parser')
    # results = soup.find_all('div', class_='fixres__item')
    results = soup.find_all('div', class_=os.environ.get('SS_SCRAPE_RESULTS'))

    for match in results[:16]:
        # if match.find(class_='matches__item-col matches__info').text.strip() != '':
        if match.find(class_=os.environ.get('SS_MATCH_INFO')).text.strip() != '':
            continue

        # home = match.find(class_='matches__participant--side1')
        home = match.find(class_=os.environ.get('SS_HOME_TEAM'))
        # away = match.find(class_='matches__participant--side2')
        away = match.find(class_=os.environ.get('SS_AWAY_TEAM'))
        all_home_matches.append(home)
        all_away_matches.append(away)

    [strip_and_add_team(match, home_fixture_list) for match in all_home_matches]
    [strip_and_add_team(match, away_fixture_list) for match in all_away_matches]

    return results


def get_all_goals_and_wins(home_team_goals):
    """
    function to determine goals scored/conceded, and the result for each game

    :param home_team_goals:
    :return:
    """

    if home_team_goals != ' - ':
        goals_scored = int(home_team_goals[:1])
        goals_conceded = int(home_team_goals[-1:])
        home_goals_scored.append(goals_scored)
        away_goals_conceded.append(goals_scored)
        home_goals_conceded.append(goals_conceded)
        away_goals_scored.append(goals_conceded)
    else:
        goals_scored = 0
        goals_conceded = 0
        home_goals_scored.append(0)
        away_goals_conceded.append(0)
        home_goals_conceded.append(0)
        away_goals_scored.append(0)

    if goals_scored > goals_conceded:
        home_team_results.append('W')
        away_team_results.append('L')
    elif goals_scored < goals_conceded:
        home_team_results.append('L')
        away_team_results.append('W')
    else:
        home_team_results.append('D')
        away_team_results.append('D')


def get_games_played(league):
    """
    function used to scrape all previous results for each team from the sky sports website, and store them in lists

    :param league:
    :return:
    """
    page = requests.get(league)
    soup = BeautifulSoup(page.content, 'html.parser')
    # results = soup.find_all('div', class_='fixres__item')
    results = soup.find_all('div', class_=os.environ.get('SS_SCRAPE_RESULTS'))

    [get_game_data(match) for match in results[:45]]


def get_game_data(match):
    """
    function to get all of the goals for teams in the selected league. The data is added to lists for manipulation

    :param match:
    :return:
    """
    # home_team = match.find(class_='matches__participant--side1')
    # away_team = match.find(class_='matches__participant--side2')
    home_team = match.find(class_=os.environ.get('SS_HOME_TEAM'))
    away_team = match.find(class_=os.environ.get('SS_AWAY_TEAM'))
    # scores = match.find_all(class_='matches__teamscores-side')
    scores = match.find_all(class_=os.environ.get('SS_MATCH_SCORES'))
    home_score = scores[0].text.strip()
    away_score = scores[1].text.strip()
    match_score = f'{home_score}:{away_score}'
    get_all_goals_and_wins(match_score)

    strip_and_add_team(home_team, home_team_list)
    strip_and_add_team(away_team, away_team_list)


def get_current_standings(league):
    """
    function to scrape the current league positions for the currently selected league

    :param league:
    :return:
    """

    page = requests.get(league)
    soup = BeautifulSoup(page.content, 'html.parser')
    # results = soup.find_all(class_='standing-table__row')
    results = soup.find_all(class_=os.environ.get('SS_LEAGUE_TABLE'))

    for team in results[:16]:
        # position = team.find('td', class_='standing-table__cell')
        position = team.find('td', class_=os.environ.get('SS_TABLE_TEAM_POSITION'))
        # team_name = team.find('td', class_='standing-table__cell--name')
        team_name = team.find('td', class_=os.environ.get('SS_TABLE_TEAM_NAME'))

        try:
            if team_name.text is not None:
                current_standings[team_name.text.strip()] = int(position.text.strip())
        except AttributeError as e:
            print(f'Error: {e}')


def convert_data():
    convert_to_dict(home_team_list, home_goals_scored, home_goals_scored_dict)
    convert_to_dict(away_team_list, away_goals_scored, away_goals_scored_dict)

    # converting team goals conceded
    convert_to_dict(home_team_list, home_goals_conceded, home_goals_conceded_dict)
    convert_to_dict(away_team_list, away_goals_conceded, away_goals_conceded_dict)

    # converting team results
    convert_to_dict(home_team_list, home_team_results, home_team_results_dict)
    convert_to_dict(away_team_list, away_team_results, away_team_results_dict)


def reset_all_value_stores():
    """
    function to reset all dictionary and list values

    :return:
    """

    home_team_list.clear()
    away_team_list.clear()

    home_goals_scored.clear()
    home_goals_conceded.clear()
    away_goals_scored.clear()
    away_goals_conceded.clear()

    home_team_results.clear()
    away_team_results.clear()
    home_team_results_dict.clear()
    away_team_results_dict.clear()

    home_goals_scored_dict.clear()
    home_goals_conceded_dict.clear()
    away_goals_scored_dict.clear()
    away_goals_conceded_dict.clear()

    total_goals_scored.clear()
    total_goals_conceded.clear()
    current_standings.clear()
