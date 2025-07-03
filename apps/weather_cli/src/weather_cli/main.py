# apps/weather_cli/src/weather_cli/main.py

import argparse
from collections import Counter

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

from .api import WeatherAPI

console = Console()


class WeatherCLI:
    """A class for displaying weather information in the command line."""

    def __init__(self):
        self.api = WeatherAPI()

    def display_weather(self, location, units="metric"):
        """Displays the current weather and forecast for a given location."""
        with Live(console=console, screen=True, redirect_stderr=False) as live:
            live.update(
                Panel("Fetching weather data...", title="[bold green]Weather Report[/bold green]")
            )

            if not location:
                location = self.api.get_location_from_ip()
                if not location:
                    return

            current_weather = self.api.get_weather(location, units)
            forecast = self.api.get_forecast(location, units)

            if not current_weather or not forecast:
                live.update(
                    Panel(
                        "[bold red]Could not retrieve weather data.[/bold red]",
                        title="[bold red]Error[/bold red]",
                    )
                )
                return

            live.update(self._generate_weather_panel(current_weather, forecast))

    def _generate_weather_panel(self, weather_data, forecast_data):
        """Generates a Rich Panel containing the weather information."""
        if weather_data.get("cod") != 200:
            return Panel(
                f"[bold red]Error:[/bold red] {weather_data.get('message', 'Could not fetch weather data.')}",
                title="[bold red]Error[/bold red]",
            )

        city = weather_data["name"]
        country = weather_data["sys"]["country"]
        main_weather = weather_data["weather"][0]["main"]
        description = weather_data["weather"][0]["description"]
        temp = weather_data["main"]["temp"]
        feels_like = weather_data["main"]["feels_like"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]
        weather_id = weather_data["weather"][0]["id"]
        emoji = self._get_weather_emoji(weather_id)

        current_weather_text = f"""
{emoji} [bold blue]{city}, {country}[/bold blue] {emoji}
Current: [bold yellow]{temp:.1f}°C[/bold yellow] (Feels like: {feels_like:.1f}°C)
Condition: {main_weather} ({description})
Humidity: {humidity}% | Wind: {wind_speed} m/s
"""

        forecast_table = self._create_forecast_table(forecast_data)

        return Panel(
            f"{current_weather_text}\n{forecast_table}",
            title="[bold green]Weather Report[/bold green]",
            border_style="green",
        )

    def _create_forecast_table(self, forecast_data):
        """Creates a Rich Table for the 5-day forecast."""
        if forecast_data.get("cod") != "200":
            return "[bold red]Could not fetch forecast data.[/bold red]"

        table = Table(
            title="[bold magenta]5-Day Forecast[/bold magenta]", style="magenta", expand=True
        )
        table.add_column("Date", style="cyan")
        table.add_column("Condition", style="green")
        table.add_column("Min/Max Temp (°C)", style="yellow", justify="right")

        daily_summaries = {}
        for item in forecast_data["list"]:
            date = item["dt_txt"].split(" ")[0]
            if date not in daily_summaries:
                daily_summaries[date] = {"temps": [], "conditions": [], "weather_ids": []}
            daily_summaries[date]["temps"].append(item["main"]["temp"])
            daily_summaries[date]["conditions"].append(item["weather"][0]["description"])
            daily_summaries[date]["weather_ids"].append(item["weather"][0]["id"])

        days_displayed = 0
        for date, summary in daily_summaries.items():
            if days_displayed >= 5:
                break
            min_temp = min(summary["temps"])
            max_temp = max(summary["temps"])
            most_common_weather_id = Counter(summary["weather_ids"]).most_common(1)[0][0]
            most_common_condition = Counter(summary["conditions"]).most_common(1)[0][0]

            table.add_row(
                date,
                f"{self._get_weather_emoji(most_common_weather_id)} {most_common_condition}",
                f"{min_temp:.1f}°C / {max_temp:.1f}°C",
            )
            days_displayed += 1

        return table

    def _get_weather_emoji(self, weather_id):
        """Returns an emoji based on OpenWeatherMap weather ID."""
        if 200 <= weather_id < 300:
            return "⛈️"
        if 300 <= weather_id < 400:
            return "🌧️"
        if 500 <= weather_id < 600:
            return "☔"
        if 600 <= weather_id < 700:
            return "❄️"
        if 700 <= weather_id < 800:
            return "🌫️"
        if weather_id == 800:
            return "☀️"
        if 801 <= weather_id < 805:
            return "☁️"
        return "❓"


def main():
    parser = argparse.ArgumentParser(description="A modern and feature-rich weather CLI.")
    parser.add_argument(
        "location",
        nargs="?",
        default=None,
        help="The city and country code to get weather for (e.g., 'London,uk').",
    )
    parser.add_argument(
        "--units",
        default="metric",
        choices=["metric", "imperial"],
        help="The units to display the temperature in.",
    )

    args = parser.parse_args()

    cli = WeatherCLI()
    cli.display_weather(args.location, args.units)


if __name__ == "__main__":
    main()
