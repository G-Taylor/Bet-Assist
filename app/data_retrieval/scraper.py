import requests
from bs4 import BeautifulSoup


def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')


league = 'https://www.skysports.com/mls-results'

page = requests.get(league)
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find_all('div', class_='fixres__item')

games = {}

for match in results[:30]:
    home = match.find(class_='matches__item-col matches__participant matches__participant--side1')
    home_team = home.find(class_='swap-text__target')
    away = match.find(class_='matches__item-col matches__participant matches__participant--side2')
    away_team = away.find(class_='swap-text__target')
    scores = match.find_all(class_='matches__teamscores-side')
    home_score = scores[0].text.strip()
    away_score = scores[1].text.strip()

    print(f'{home_team.text}  {home_score} : {away_score}  {away_team.text}')


# print(all_home_matches)

