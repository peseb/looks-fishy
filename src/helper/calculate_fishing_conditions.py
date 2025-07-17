from typing import Callable, List, Optional
from weather_forecast.weather_response import NextHours, Timeserie, TimeserieData


def get_most_accurate_nexthours(data: TimeserieData) -> Optional[NextHours]:
    if data.next_1_hours is not None:
        return data.next_1_hours
    if data.next_6_hours is not None:
        return data.next_6_hours
    return data.next_12_hours


def nexthours_has_condition(data: TimeserieData, condition: str):
    nextHours = get_most_accurate_nexthours(data)
    if nextHours is None:
        return False

    return condition in nextHours.summary.symbol_code


def day_has_condition(day_info: List[Timeserie], condition: str):
    result = len(
        list(
            filter(
                lambda x: nexthours_has_condition(x.data, condition),
                day_info,
            )
        )
    )

    print(f"Hours {condition}: {result}")
    return result


def has_instant_condition(
    day_info: List[Timeserie],
    check_condition: Callable[[Timeserie], bool],
    condition_description: str,
):
    result = len(
        list(
            filter(
                lambda x: check_condition(x),
                day_info,
            )
        )
    )

    print(f"Hours {condition_description}: {result}")
    return result


# Possible conditions can be found here: https://github.com/metno/weathericons/tree/main/weather
def calculate_fishing_conditions(day_info: List[Timeserie]):
    hours_good_conditions = 1
    hours_bad_conditions = 1

    # Light rain is good
    hours_light_rain = day_has_condition(day_info, "lightrain")
    hours_good_conditions += hours_light_rain

    # Cloud cover is good
    hours_cloudy = day_has_condition(day_info, "cloud")
    hours_good_conditions += hours_cloudy

    # Direct sun not so good
    hours_direct_sun = day_has_condition(day_info, "clearsky_day")
    hours_bad_conditions += hours_direct_sun

    # heavy rain not so good?
    hours_heavy_rain = day_has_condition(day_info, "heavyrain")
    hours_bad_conditions += hours_heavy_rain

    # thunder not so good?
    hours_thunder = day_has_condition(day_info, "thunder")
    hours_bad_conditions += hours_thunder

    # Documentation for wind direction: https://api.met.no/weatherapi/locationforecast/2.0/documentation
    # Wind from north not so good
    def wind_from_north(serie: Timeserie):
        return serie.data.instant.details.wind_from_direction < 90

    hours_north_wind = has_instant_condition(
        day_info, wind_from_north, "wind from north"
    )
    hours_bad_conditions += hours_north_wind

    # Wind from east or southeast good
    def wind_from_southeast(serie: Timeserie):
        return (
            serie.data.instant.details.wind_from_direction > 90
            and serie.data.instant.details.wind_from_direction <= 180
        )

    hours_southeast_wind = has_instant_condition(
        day_info, wind_from_southeast, "wind from southeast"
    )
    hours_good_conditions += hours_southeast_wind

    # Wind: no wind not good
    def no_wind(serie: Timeserie):
        return serie.data.instant.details.wind_speed <= 0.5

    hours_no_wind = has_instant_condition(day_info, no_wind, "no wind")
    hours_bad_conditions += hours_no_wind

    # Wind: too much wind not good
    def to_much_wind(serie: Timeserie):
        return serie.data.instant.details.wind_speed >= 10

    hours_to_much_wind = has_instant_condition(day_info, to_much_wind, "too much wind")
    hours_bad_conditions += hours_to_much_wind

    # Wind: a little windy good
    def ideal_wind(serie: Timeserie):
        return (
            serie.data.instant.details.wind_speed >= 1
            and serie.data.instant.details.wind_speed <= 5
        )

    hours_ideal_wind = has_instant_condition(day_info, ideal_wind, "ideal wind")
    hours_good_conditions += hours_ideal_wind

    # Good temp: Between 10-20
    def good_temperature(serie: Timeserie):
        return (
            serie.data.instant.details.air_temperature >= 15
            and serie.data.instant.details.air_temperature <= 25
        )

    hours_good_temperature = has_instant_condition(
        day_info, good_temperature, "good temperature"
    )
    hours_good_conditions += hours_good_temperature

    # Bad temp: Outside of 10-20
    def bad_temperature(serie: Timeserie):
        return (
            serie.data.instant.details.air_temperature < 15
            or serie.data.instant.details.air_temperature > 25
        )

    hours_bad_temperature = has_instant_condition(
        day_info, bad_temperature, "bad temperature"
    )
    hours_bad_conditions += hours_bad_temperature

    return hours_good_conditions / hours_bad_conditions
