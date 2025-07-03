# apps/job_scraper/src/job_scraper/scraper.py

import csv
import argparse
from rich.console import Console
from rich.progress import Progress
from shared_utils.scraper_utils import get_soup

console = Console()

class JobScraper:
    """A class for scraping job listings from Indeed.com."""

    def __init__(self, site="indeed"):
        self.site = site
        self.base_url = "https://www.indeed.com"

    def scrape(self, keyword, location, num_pages=1):
        """Scrapes job listings for a given keyword and location."""
        console.print(f"[bold green]Scraping {self.site} for '{keyword}' jobs in '{location}'...[/bold green]")
        job_listings = []
        with Progress(console=console) as progress:
            task = progress.add_task("[green]Scraping pages...[/green]", total=num_pages)
            for page in range(num_pages):
                url = self.construct_url(keyword, location, page)
                soup = get_soup(url, headers={"User-Agent": "Mozilla/5.0"})
                if soup:
                    job_listings.extend(self.parse_jobs(soup))
                progress.update(task, advance=1)
        return job_listings

    def construct_url(self, keyword, location, page):
        """Constructs the URL for the job search query."""
        return f"{self.base_url}/jobs?q={keyword}&l={location}&start={page * 10}"

    def parse_jobs(self, soup):
        """Parses the job listings from the BeautifulSoup object."""
        jobs = []
        for job_card in soup.find_all("div", class_="job_seen_beacon") :
            title = job_card.find("h2", class_="jobTitle").text.strip()
            company = job_card.find("span", class_="companyName").text.strip()
            link = self.base_url + job_card.find("a", class_="jcs-JobTitle")["href"]
            jobs.append({"title": title, "company": company, "link": link})
        return jobs

    def save_to_csv(self, jobs, output_file):
        """Saves the job listings to a CSV file."""
        if not jobs:
            console.print("[bold yellow]No jobs found to save.[/bold yellow]")
            return

        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["title", "company", "link"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(jobs)
        console.print(f"[bold green]Scraping complete. Data saved to[/bold green] [cyan]{output_file}[/cyan]")

def main():
    parser = argparse.ArgumentParser(description="A powerful and extensible job scraper.")
    parser.add_argument("keyword", help="The job keyword to search for.")
    parser.add_argument("location", help="The location to search in.")
    parser.add_argument("--site", default="indeed", help="The job board to scrape (currently only 'indeed' is supported).")
    parser.add_argument("--pages", type=int, default=1, help="The number of pages to scrape.")
    parser.add_argument("--output", default="jobs.csv", help="The output CSV file.")
    
    args = parser.parse_args()

    scraper = JobScraper(site=args.site)
    jobs = scraper.scrape(args.keyword, args.location, num_pages=args.pages)
    scraper.save_to_csv(jobs, args.output)

if __name__ == "__main__":
    main()