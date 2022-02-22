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


# function to strip useless info and text, and add teams to list
def strip_and_add_team(team, team_list):
    if team is not None:
        team = team.text.strip(" * ()1234567890").split(' (')
        team_list.append(team[0])


# function to convert any two lists into a dictionary
def convert_to_dict(team_list, goal_list, results_dict):
    res = [(team_list[i], goal_list[i]) for i in range(0, len(team_list))]

    for team, goals in res:
        results_dict.setdefault(team, []).append(goals)


# function to merge dictionaries together
def merge_dict(dict1, dict2):
    dict3 = {**dict1, **dict2}
    for key, value in dict3.items():
        if key in dict1 and key in dict2:
            dict3[key] = [value, dict1[key]]
    return dict3


# function used to get upcoming fixtures
def get_fixtures(league):
    page = requests.get(league)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='national')

    all_home_matches = results.find_all('td', class_='home uc')
    all_away_matches = results.find_all('td', class_='away uc')

    for match in all_home_matches:
        strip_and_add_team(match, home_fixture_list)

    for match in all_away_matches:
        strip_and_add_team(match, away_fixture_list)


# function to gather goals scored/conceded, and the result
def get_all_goals_and_wins(home_team_goals):
    if home_team_goals.text != ' - ':
        goals_scored = int(home_team_goals.text[:1])
        goals_conceded = int(home_team_goals.text[-1:])
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


# function used to scrape all previous results for each team from the web, and store them in lists
def get_games_played(league):
    # because of the website that info is scraped from, even rows of tables are done first, then odd rows
    page = requests.get(league)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='national')

    even_matches = results.find_all('tr', class_='even')
    odd_matches = results.find_all('tr', class_='odd')

    for match in even_matches:
        home_team = match.find('td', class_='home uc')
        home_team_win = match.find('td', class_='home uc winteam')
        home_team_goals = match.find('a', class_='score_link')
        away_team = match.find('td', class_='away uc')
        away_team_win = match.find('td', class_='away uc winteam')

        get_all_goals_and_wins(home_team_goals)

        strip_and_add_team(home_team, home_team_list)
        strip_and_add_team(home_team_win, home_team_list)
        strip_and_add_team(away_team, away_team_list)
        strip_and_add_team(away_team_win, away_team_list)

    for match in odd_matches:
        home_team = match.find('td', class_='home uc')
        home_team_win = match.find('td', class_='home uc winteam')
        home_team_goals = match.find('a', class_='score_link')
        away_team = match.find('td', class_='away uc')
        away_team_win = match.find('td', class_='away uc winteam')

        get_all_goals_and_wins(home_team_goals)

        strip_and_add_team(home_team, home_team_list)
        strip_and_add_team(home_team_win, home_team_list)
        strip_and_add_team(away_team, away_team_list)
        strip_and_add_team(away_team_win, away_team_list)


def convert_data():
    convert_to_dict(home_team_list, home_goals_scored, home_goals_scored_dict)
    convert_to_dict(away_team_list, away_goals_scored, away_goals_scored_dict)

    # converting team goals conceded
    convert_to_dict(home_team_list, home_goals_conceded, home_goals_conceded_dict)
    convert_to_dict(away_team_list, away_goals_conceded, away_goals_conceded_dict)

    # converting team results
    convert_to_dict(home_team_list, home_team_results, home_team_results_dict)
    convert_to_dict(away_team_list, away_team_results, away_team_results_dict)

# def get_last_results(result):
#     team_list = []
#
#     for team in all_results_dict:
#         result_list = []
#         result_list += all_results_dict[team][0]
#         result_list += all_results_dict[team][1]
#         # total_results = result_list + result_list2
#
#         if result == 'won' and result_list.count('W') >= 4:
#             team_list.append(team)
#         elif result == 'lost' and result_list.count('L') >= 3:
#             team_list.append(team)
#         elif result == 'draw' and result_list.count('D') >= 3:
#             team_list.append(team)
#
#     return team_list
#
#
# def get_total_goals(team_name, goal_dict):
#     try:
#         goals = sum(goal_dict[team_name][1])
#     except IndexError:
#         goals = sum(goal_dict[team_name])
#         return goals
#     else:
#         goals += sum(goal_dict[team_name][0])
#         return goals
#
#
# def get_dict_length(team_name, goal_dict):
#     try:
#         length = len(goal_dict[team_name][1])
#     except IndexError:
#         length = len(goal_dict[team_name])
#         return length
#     else:
#         length += len(goal_dict[team_name][0])
#         return length
#
#
# def get_average_goals(goal_dict):
#     for team in goal_dict:
#         total_goals = get_total_goals(team, goal_dict)
#         avg_goals = total_goals / len(goal_dict)
#         return avg_goals