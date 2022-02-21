# fixture URLS
WEBSITE_URL = 'https://www.scorespro.com/soccer/'
leagues = {
    'PREM': 'england/premier-league/',
    'CHAMPIONSHIP': 'england/championship/',
    'LEAGUE1': 'england/league-one/',
    'LEAGUE2': 'england/league-two/',
    'NATIONAL': 'england/national-league/',
    'SCOT': 'scotland/premiership/',
    'SPANISH': 'spain/laliga/',
    'GERMAN': 'germany/bundesliga/',
    'ITALIAN': 'italy/serie-a/',
    'FRENCH': 'france/ligue-1/',
    'DUTCH': 'netherlands/eredivisie/',
    'CL': 'uefa/champions-league/',
    'EUROPA': 'uefa/europa-league/',
}


def get_league():
    for name in leagues:
        print(name)

    selection = input("Select League: ").upper()

    for name in leagues:
        if name == selection:
            return f'{WEBSITE_URL}{leagues[name]}'
