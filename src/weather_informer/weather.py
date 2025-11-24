import requests
import logging

from dotenv import load_dotenv
import os

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

logger = logging.getLogger(__name__)

def get_weather(city: str) -> str:
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "ru"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if response.status_code == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"].capitalize()
            city_name = data["name"]
            country = data["sys"]["country"]
            return f"🌤 Погода в {city_name}, {country}:\n🌡 {temp}°C\n📜 {description}"
        else:
            return "❌ Не удалось получить погоду. Проверьте название города."
    except Exception as e:
        logger.error(f"Ошибка при запросе погоды для '{city}': {e}")
        return "⚠️ Произошла ошибка при получении погоды."
