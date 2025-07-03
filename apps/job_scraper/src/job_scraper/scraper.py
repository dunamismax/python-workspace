import requests
from bs4 import BeautifulSoup
import csv
import sys
from rich.console import Console
from rich.progress import Progress

console = Console()

def scrape_job_board(url, keyword, output_file="jobs.csv"):
    """Scrapes a job board for listings and saves them to a CSV file."""
    console.print(f"[bold green]Scraping[/bold green] [cyan]{url}[/cyan] [bold green]for keyword:[/bold green] [yellow]{keyword}[/yellow]")
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Error fetching URL:[/bold red] {e}")
        return

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
    dummy_jobs = [
        {'title': f'Software Engineer - {keyword}', 'company': 'Tech Corp', 'link': 'http://example.com/job1'},
        {'title': f'Junior Developer - {keyword}', 'company': 'Startup Inc.', 'link': 'http://example.com/job2'},
        {'title': f'Data Scientist - {keyword}', 'company': 'Data Insights', 'link': 'http://example.com/job3'},
    ]

    with Progress(console=console) as progress:
        task = progress.add_task("[green]Processing job listings...[/green]", total=len(dummy_jobs))
        for job in dummy_jobs:
            job_listings.append(job)
            progress.update(task, advance=1, description=f"[green]Found[/green] [yellow]'{job['title']}'[/yellow]")

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'company', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(job_listings)

    console.print(f"[bold green]Scraping complete. Data saved to[/bold green] [cyan]{output_file}[/cyan]")

if __name__ == '__main__':
    if len(sys.argv) == 4:
        url = sys.argv[1]
        keyword = sys.argv[2]
        output_file = sys.argv[3]
        scrape_job_board(url, keyword, output_file)
    else:
        console.print("[bold red]Usage: python -m job_scraper.scraper <url> <keyword> <output_file>[/bold red]")
        console.print("[bold yellow]Example: python -m job_scraper.scraper http://example.com/jobs Python jobs.csv[/bold yellow]")
