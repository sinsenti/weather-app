import os
import requests
from flask import current_app

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"


def fetch_weather(city):
    if not OPENWEATHER_API_KEY:
        raise ValueError("OPENWEATHER_API_KEY is not set.")

    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
    }

    try:
        response = requests.get(OPENWEATHER_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("cod") != 200:
            return None, data.get("message", "Unexpected API error")

        main_info = data.get("main", {})
        weather_details = data.get("weather", [{}])[0]

        weather_data = {
            "temperature": main_info.get("temp"),
            "weather_description": weather_details.get("description"),
            "humidity": main_info.get("humidity"),
            "wind_speed": data.get("wind", {}).get("speed"),
        }

        return weather_data, None

    except requests.RequestException as e:
        current_app.logger.error(f"Error fetching weather data: {e}")
        return None, str(e)
