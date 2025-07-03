import os
import requests
import inquirer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Rich Console
console = Console()

# OpenWeatherMap API Key
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast?"

def get_weather_data(location):
    """Fetches current weather data for a given location."""
    complete_url = f"{BASE_URL}q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(complete_url)
    return response.json()

def get_forecast_data(location):
    """Fetches 5-day weather forecast data for a given location."""
    complete_url = f"{FORECAST_URL}q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(complete_url)
    return response.json()

def get_weather_emoji(weather_id):
    """Returns an emoji based on OpenWeatherMap weather ID."""
    if 200 <= weather_id < 300:
        return "⛈️"  # Thunderstorm
    elif 300 <= weather_id < 400:
        return "🌧️"  # Drizzle
    elif 500 <= weather_id < 600:
        return "☔"  # Rain
    elif 600 <= weather_id < 700:
        return "❄️"  # Snow
    elif 700 <= weather_id < 800:
        return "🌫️"  # Atmosphere (mist, smoke, haze, dust, fog, sand, ash, squall, tornado)
    elif weather_id == 800:
        return "☀️"  # Clear
    elif 801 <= weather_id < 805:
        return "☁️"  # Clouds
    else:
        return "❓"  # Unknown

def display_current_weather(weather_data):
    """Displays current weather information using Rich."""
    if weather_data.get("cod") != 200:
        console.print(f"[bold red]Error:[/bold red] {weather_data.get('message', 'Could not fetch weather data.')}")
        return

    city = weather_data["name"]
    country = weather_data["sys"]["country"]
    main_weather = weather_data["weather"][0]["main"]
    description = weather_data["weather"][0]["description"]
    temp = weather_data["main"]["temp"]
    feels_like = weather_data["main"]["feels_like"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    weather_id = weather_data["weather"][0]["id"]
    emoji = get_weather_emoji(weather_id)

    panel_content_str = f"""
{emoji} [bold blue]{city}, {country}[/bold blue] {emoji}
Current: [bold yellow]{temp:.1f}°C[/bold yellow] (Feels like: {feels_like:.1f}°C)
Condition: {main_weather} ({description})
Humidity: {humidity}% | Wind: {wind_speed} m/s
"""
    panel_content = Text.from_markup(panel_content_str, justify="center")

    console.print(Panel(panel_content, title="[bold green]Current Weather[/bold green]", border_style="green"))

def display_forecast(forecast_data):
    """Displays 5-day weather forecast using Rich Table."""
    if forecast_data.get("cod") != "200":
        console.print(f"[bold red]Error:[/bold red] {forecast_data.get('message', 'Could not fetch forecast data.')}")
        return

    table = Table(title="[bold magenta]5-Day Forecast[/bold magenta]", style="magenta", expand=True)
    table.add_column("Date", style="cyan")
    table.add_column("Condition", style="green")
    table.add_column("Min/Max Temp (°C)", style="yellow", justify="right")

    # Group forecast by day and extract relevant info
    daily_summaries = {}
    for item in forecast_data["list"]:
        date = item["dt_txt"].split(" ")[0]
        if date not in daily_summaries:
            daily_summaries[date] = {
                "temps": [],
                "conditions": [],
                "weather_ids": []
            }
        daily_summaries[date]["temps"].append(item["main"]["temp"])
        daily_summaries[date]["conditions"].append(item["weather"][0]["description"])
        daily_summaries[date]["weather_ids"].append(item["weather"][0]["id"])

    # Display forecast for up to 5 days
    days_displayed = 0
    for date, summary in daily_summaries.items():
        if days_displayed >= 5:
            break
        min_temp = min(summary["temps"])
        max_temp = max(summary["temps"])

        from collections import Counter
        most_common_weather_id = Counter(summary["weather_ids"]).most_common(1)[0][0]
        representative_emoji = get_weather_emoji(most_common_weather_id)
        most_common_condition = Counter(summary["conditions"]).most_common(1)[0][0]

        table.add_row(
            date,
            f"{most_common_condition}",
            f"{min_temp:.1f}°C / {max_temp:.1f}°C"
        )
        days_displayed += 1

    console.print(table)

def main():
    questions = [
        inquirer.Text("zip_code", message="Enter zip code (e.g., 90210 for US)"),
    ]
    answers = inquirer.prompt(questions)

    if answers and answers["zip_code"]:
        zip_code = answers["zip_code"]
        # OpenWeatherMap API requires country code for zip code queries. Defaulting to US.
        location_query = f"{zip_code},us"
        console.print(f"Fetching weather for zip code [bold]{zip_code}[/bold]...")

        current_weather = get_weather_data(location_query)
        display_current_weather(current_weather)

        forecast = get_forecast_data(location_query)
        display_forecast(forecast)
    else:
        console.print("[bold red]No zip code entered. Exiting.[/bold red]")

if __name__ == "__main__":
    main()
