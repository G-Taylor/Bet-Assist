import unittest
import requests
from app.league_info.league_urls import leagues


class UrlTests(unittest.TestCase):

    # Test base url for scraping data returns a 200 response
    def test_base_web_url(self):
        url = 'https://www.skysports.com/'
        page = requests.get(url)
        self.assertEqual(page.status_code, 200)

    def test_league_result_urls(self):
        for league in leagues:
            print(f'Testing league results url for {league}')
            url = f'https://www.skysports.com/{leagues[league]}-results'
            page = requests.get(url)
            self.assertEqual(page.status_code, 200)

    def test_league_fixture_urls(self):
        for league in leagues:
            print(f'Testing league fixtures url for {league}')
            url = f'https://www.skysports.com/{leagues[league]}-fixtures'
            page = requests.get(url)
            self.assertEqual(page.status_code, 200)


if __name__ == '__main__':
    unittest.main()
