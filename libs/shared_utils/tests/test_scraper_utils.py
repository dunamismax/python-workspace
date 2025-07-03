# libs/shared_utils/tests/test_scraper_utils.py

import unittest
from unittest.mock import patch, MagicMock
import requests
from shared_utils.scraper_utils import get_soup

class TestScraperUtils(unittest.TestCase):

    @patch('requests.get')
    def test_get_soup_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test</title></head><body><p>Hello</p></body></html>"
        mock_get.return_value = mock_response

        soup = get_soup("http://example.com")
        self.assertIsNotNone(soup)
        self.assertEqual(soup.title.string, "Test")

    @patch('requests.get')
    def test_get_soup_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Test error")
        soup = get_soup("http://example.com")
        self.assertIsNone(soup)

if __name__ == '__main__':
    unittest.main()
