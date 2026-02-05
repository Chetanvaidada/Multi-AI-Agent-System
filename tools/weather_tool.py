import os
import requests
from langchain.tools import tool
from dotenv import load_dotenv
load_dotenv()

BASE_URL = "http://api.weatherapi.com/v1/current.json"
@tool
def get_weather(city: str):
    """
    Fetch current weather for a given city using WeatherAPI.com

    Args:
        city (str): City name (e.g., "Mumbai")

    Returns:
        dict: Weather details
    """
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "WEATHER_API_KEY not found. Please set it in your .env file."
        )

    params = {
        "key": api_key,
        "q": city,
        "aqi": "no"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {
            "city": city,
            "error": str(e)
        }

    data = response.json()

    return {
        "city": data["location"]["name"],
        "country": data["location"]["country"],
        "temperature_celsius": data["current"]["temp_c"],
        "feels_like_celsius": data["current"]["feelslike_c"],
        "humidity": data["current"]["humidity"],
        "condition": data["current"]["condition"]["text"],
        "wind_kph": data["current"]["wind_kph"]
    }
