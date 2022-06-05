import requests
from bs4 import BeautifulSoup

page = requests.get('https://www.365scores.com/en-uk/football/usa/mls/league/104#results')
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find_all('div', class_='entity-scores-widget-group_container__3xiqL')

# for game in results:
#     teams = game.find_all('div', class_='game-card-competitor_name__1h_Ng')
#     home_team = teams[0]
#     away_team = teams[1]
#     print(f'{home_team.text} : {away_team.text}')
print(soup)