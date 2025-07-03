# apps/weather_cli/tests/test_main.py

import unittest
from unittest.mock import patch, MagicMock
from weather_cli.main import WeatherCLI

class TestWeatherCLI(unittest.TestCase):

    @patch('weather_cli.api.WeatherAPI')
    def test_display_weather(self, MockWeatherAPI):
        # Mock the API responses
        mock_api_instance = MockWeatherAPI.return_value
        mock_api_instance.get_weather.return_value = {
            "cod": 200, "name": "Test City", "sys": {"country": "TC"},
            "weather": [{"main": "Clear", "description": "clear sky", "id": 800}],
            "main": {"temp": 25, "feels_like": 26, "humidity": 50},
            "wind": {"speed": 5}
        }
        mock_api_instance.get_forecast.return_value = {
            "cod": "200", "list": []
        }

        cli = WeatherCLI()
        # We can't easily test the Rich Live display, so we'll just check that it runs without error
        try:
            cli.display_weather("Test City,TC")
        except Exception as e:
            self.fail(f"display_weather raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
