from requests import get
from bs4 import BeautifulSoup

page = get('https://www.skysports.com/premier-league-results')
soup = BeautifulSoup(page.text, 'html.parser')
matches = soup.find_all('div', class_='fixres__item')
print(type(matches))
print(len(matches))
first_match = matches[0]
home_team = first_match.find('span', class_='matches__item-col matches__participant matches__participant--side1').text
home_team = home_team.strip()

team2 = first_match.find('span', class_='matches__item-col matches__participant matches__participant--side2').text
team2 = home_team.strip()
print(home_team)
print(team2)
# results = soup.find(id='national')
#
# even_matches = results.find_all('tr', class_='even')
# odd_matches = results.find_all('tr', class_='odd')