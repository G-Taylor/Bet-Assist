import unittest
import requests


class UrlTestCase(unittest.TestCase):

    # Test base url for scraping data returns a 200 response
    def test_base_web_url(self):
        url = 'https://www.skysports.com/'
        page = requests.get(url)
        self.assertEqual(page.status_code, 200)


if __name__ == '__main__':
    unittest.main()
