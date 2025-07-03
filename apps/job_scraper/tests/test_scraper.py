# apps/job_scraper/tests/test_scraper.py

import unittest
from unittest.mock import patch, MagicMock
from job_scraper.scraper import JobScraper
import os
from bs4 import BeautifulSoup

class TestJobScraper(unittest.TestCase):

    def get_mock_soup(self):
        html = """
        <div class="job_seen_beacon">
            <h2 class="jobTitle"><a>Software Engineer</a></h2>
            <span class="companyName">Tech Company</span>
            <a class="jcs-JobTitle" href="/job/123"></a>
        </div>
        """
        return BeautifulSoup(html, 'html.parser')

    @patch('job_scraper.scraper.get_soup')
    def test_scrape(self, mock_get_soup):
        # Mock the response from get_soup
        mock_get_soup.return_value = self.get_mock_soup()

        scraper = JobScraper()
        jobs = scraper.scrape("python", "remote")
        
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]['title'], 'Software Engineer')
        self.assertEqual(jobs[0]['company'], 'Tech Company')
        self.assertTrue(jobs[0]['link'].endswith("/job/123"))

    def test_save_to_csv(self):
        scraper = JobScraper()
        jobs = [{'title': 'Dev', 'company': 'Inc', 'link': 'example.com'}]
        output_file = "test_jobs.csv"
        scraper.save_to_csv(jobs, output_file)
        
        self.assertTrue(os.path.exists(output_file))
        with open(output_file, 'r') as f:
            self.assertIn("Dev,Inc,example.com", f.read())
        os.remove(output_file)

if __name__ == '__main__':
    unittest.main()
