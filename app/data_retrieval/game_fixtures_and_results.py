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
        # team_name = team.find('a')
        team_name = team.find(class_='swap-text__target')
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


def merge_dict(dict1, dict2):
    """
    function to merge dictionaries together

    :param dict1:
    :param dict2:
    :return:
    """

    dict3 = {**dict1, **dict2}
    for key, value in dict3.items():
        if key in dict1 and key in dict2:
            dict3[key] = [value, dict1[key]]
    return dict3


def get_fixtures(league):
    """
    function to scrape upcoming fixtures from source website

    :param league:
    :return:
    """
    # TODO: Fix fixture retrieval for sky sports
    page = requests.get(league)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='national')

    all_home_matches = results.find_all('td', class_='home uc')
    all_away_matches = results.find_all('td', class_='away uc')

    [strip_and_add_team(match, home_fixture_list) for match in all_home_matches]
    [strip_and_add_team(match, away_fixture_list) for match in all_away_matches]


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
    function used to scrape all previous results for each team from the web, and store them in lists

    :param league:
    :return:
    """

    # because of the website that info is scraped from, even rows of tables are done first, then odd rows
    page = requests.get(league)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', class_='fixres__item')

    # even_matches = results.find_all('tr', class_='even')
    # odd_matches = results.find_all('tr', class_='odd')

    # [get_game_data(match) for match in even_matches]
    # [get_game_data(match) for match in odd_matches]
    [get_game_data(match) for match in results[:40]]


def get_game_data(match):
    """
    function to get all of the goals for teams in the selected league. The data is added to lists for manipulation

    :param match:
    :return:
    """

    # home_team = match.find('td', class_='home uc')
    # home_team_win = match.find('td', class_='home uc winteam')
    # home_team_goals = match.find('a', class_='score_link')
    # away_team = match.find('td', class_='away uc')
    # away_team_win = match.find('td', class_='away uc winteam')

    home_team = match.find(class_='matches__item-col matches__participant matches__participant--side1')
    away_team = match.find(class_='matches__item-col matches__participant matches__participant--side2')
    scores = match.find_all(class_='matches__teamscores-side')
    home_score = scores[0].text.strip()
    away_score = scores[1].text.strip()
    match_score = f'{home_score}:{away_score}'
    get_all_goals_and_wins(match_score)

    strip_and_add_team(home_team, home_team_list)
    # strip_and_add_team(home_team_win, home_team_list)
    strip_and_add_team(away_team, away_team_list)
    # strip_and_add_team(away_team_win, away_team_list)


def get_current_standings(league):
    """
    function to scrape the current league positions for the currently selected league

    :param league:
    :return:
    """

    page = requests.get(league)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all(class_='standing-table__row')
    # all_standings = results.find_all('tr', class_='sp-livetable__tableRow spm-dataRow')

    for team in results[1:]:
        # team_name = team.find('div', class_='sp-livetable__tableTeamName')
        # position = team.find('div', class_='sp-livetable__tablePosNum')
        position = team.find('td', class_='standing-table__cell')
        team_name = team.find('td', class_='standing-table__cell--name')

        if team_name.text is not None:
            current_standings[team_name.text] = int(position.text)


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
