import json
from helper.calculate_fishing_conditions import calculate_fishing_conditions
from helper.is_data_for_date import date_from_str, is_data_for_date
from weather_forecast.weather_response import WeatherResponse


def get_mock_data():
    file = open("src/tests/mock_data/weather_data.json", "r")
    content = json.loads(file.read())
    file.close()
    return WeatherResponse(**content)


def test_read_mock_data():
    mock_weather = get_mock_data()
    assert len(mock_weather.properties.timeseries) == 86


def test_calculate_conditions():
    mock_weather = get_mock_data()
    day = date_from_str("2025-07-14T10:27:27Z")
    day_info = list(
        filter(
            lambda x: is_data_for_date(x.time, day),
            mock_weather.properties.timeseries,
        )
    )
    result = calculate_fishing_conditions(day_info)
    assert result == 1
