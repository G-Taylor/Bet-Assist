from dateutil.parser import parse


class GetMatchDateAndTime:

    def __init__(self):
        pass

    @staticmethod
    def get_date_and_time(fixture_scrape_data, team1, team2):
        try:
            for match in fixture_scrape_data[:16]:
                home = match.find(class_='matches__participant--side1')
                away = match.find(class_='matches__participant--side2')

                if home.text.strip() == team1 and away.text.strip() == team2:
                    date = home.find_previous('h4').text
                    parsed_date = parse(date).date()
                    time = match.find(class_='matches__date').text.strip()
                    return date, time, parsed_date
        except TypeError as e:
            print(f'Error getting date/time from scrape - {e}')
