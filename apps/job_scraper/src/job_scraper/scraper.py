import requests
from bs4 import BeautifulSoup
import csv

def scrape_job_board(url, keyword, output_file="jobs.csv"):
    """Scrapes a job board for listings and saves them to a CSV file."""
    print(f"Scraping {url} for keyword: {keyword}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    job_listings = []
    # This is a placeholder. You'll need to inspect the actual job board's HTML
    # to find the correct tags and classes for job titles, companies, and links.
    # Example: for job_card in soup.find_all('div', class_='job-card'):
    #            title = job_card.find('h2', class_='job-title').text.strip()
    #            company = job_card.find('span', class_='company-name').text.strip()
    #            link = job_card.find('a', class_='job-link')['href']
    #            job_listings.append({'title': title, 'company': company, 'link': link})

    # For demonstration, let's add some dummy data
    job_listings.append({
        'title': f'Software Engineer - {keyword}',
        'company': 'Tech Corp',
        'link': 'http://example.com/job1'
    })
    job_listings.append({
        'title': f'Junior Developer - {keyword}',
        'company': 'Startup Inc.',
        'link': 'http://example.com/job2'
    })

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'company', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for job in job_listings:
            writer.writerow(job)

    print(f"Scraping complete. Data saved to {output_file}")

if __name__ == '__main__':
    # Example usage: python -m job_scraper.scraper
    # This will create a jobs.csv in the current directory
    scrape_job_board("http://example.com/jobs", "Python")
