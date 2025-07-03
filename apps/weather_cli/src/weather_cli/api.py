# apps/weather_cli/src/weather_cli/api.py

import os
import requests
from rich.console import Console
from dotenv import load_dotenv

load_dotenv()
console = Console()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5"

class WeatherAPI:
    """A class for interacting with the OpenWeatherMap API."""

    def __init__(self):
        if not OPENWEATHER_API_KEY:
            raise ValueError("OPENWEATHER_API_KEY is not set in the environment variables.")

    def get_weather(self, location, units="metric"):
        """Fetches the current weather data for a given location."""
        url = f"{BASE_URL}/weather?q={location}&appid={OPENWEATHER_API_KEY}&units={units}"
        return self._make_request(url)

    def get_forecast(self, location, units="metric"):
        """Fetches the 5-day weather forecast for a given location."""
        url = f"{BASE_URL}/forecast?q={location}&appid={OPENWEATHER_API_KEY}&units={units}"
        return self._make_request(url)

    def get_location_from_ip(self):
        """Determines the user's location based on their IP address."""
        try:
            response = requests.get("https://ipinfo.io/json")
            response.raise_for_status()
            data = response.json()
            return f"{data['city']},{data['country']}"
        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]Error getting location from IP: {e}[/bold red]")
            return None

    def _make_request(self, url):
        """Makes a request to the OpenWeatherMap API and returns the JSON response."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]Error making API request: {e}[/bold red]")
            return None
