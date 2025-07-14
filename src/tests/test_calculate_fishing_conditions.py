import json
from weather_forecast.weather_response import WeatherResponse


def get_mock_data():
    file = open("src/tests/mock_data/weather_data.json", "r")
    content = json.loads(file.read())
    file.close()
    return WeatherResponse(**content)


def test_read_mock_data():
    mock_weather = get_mock_data()
    assert len(mock_weather.properties.timeseries) == 86
