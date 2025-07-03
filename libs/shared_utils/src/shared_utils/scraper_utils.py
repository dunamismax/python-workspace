# libs/shared_utils/src/shared_utils/scraper_utils.py

import requests
from bs4 import BeautifulSoup
from rich.console import Console

console = Console()

def get_soup(url, headers=None):
    """Fetches the content of a URL and returns a BeautifulSoup object."""
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Error fetching URL {url}: {e}[/bold red]")
        return None
