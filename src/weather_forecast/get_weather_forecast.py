from typing import Optional
import requests
from location_search.search_result import Location
from weather_forecast.weather_response import WeatherResponse


def get_weather_forecast(location: Location) -> Optional[WeatherResponse]:
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={location.representasjonspunkt.nord}&lon={location.representasjonspunkt.øst}"
    headers = {
        "User-Agent": "Looks-Fishy",
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return WeatherResponse(**data)
    except Exception as e:
        print(f"Error during API request: {e}")
