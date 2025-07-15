from typing import Callable, List, Optional
from weather_forecast.weather_response import NextHours, Timeserie


def nexthours_has_condition(nextHours: Optional[NextHours], condition: str):
    if nextHours is None:
        return False

    return condition in nextHours.summary.symbol_code


def day_has_condition(day_info: List[Timeserie], condition: str):
    result = (
        len(
            list(
                filter(
                    lambda x: nexthours_has_condition(x.data.next_1_hours, condition),
                    day_info,
                )
            )
        )
        > 0
        or len(
            list(
                filter(
                    lambda x: nexthours_has_condition(x.data.next_6_hours, condition),
                    day_info,
                )
            )
        )
        > 0
        or len(
            list(
                filter(
                    lambda x: nexthours_has_condition(x.data.next_12_hours, condition),
                    day_info,
                )
            )
        )
        > 0
    )

    print(f"Has {condition}: {result}")
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

    print(f"Has {condition_description}: {result} hours")
    return result


# Possible conditions can be found here: https://github.com/metno/weathericons/tree/main/weather
def calculate_fishing_conditions(day_info: List[Timeserie]):
    good_conditions = 1
    bad_conditions = 1

    ## General conditions ##

    # Light rain is good
    has_light_rain = day_has_condition(day_info, "lightrain")
    if has_light_rain:
        good_conditions += 1

    # Cloud cover is good
    is_cloudy = day_has_condition(day_info, "cloud")
    if is_cloudy:
        good_conditions += 1

    # Direct sun not so good
    has_direct_sun = day_has_condition(day_info, "clearsky_day")
    if has_direct_sun:
        bad_conditions += 1

    # heavy rain not so good?
    has_heavy_rain = day_has_condition(day_info, "heavyrain")
    if has_heavy_rain:
        bad_conditions += 1

    # thunder not so good?
    has_thunder = day_has_condition(day_info, "thunder")
    if has_thunder:
        bad_conditions += 1

    ## Hourly conditions ##

    # Wind: Vindretningen har stor påvirkning på ørretfiske. Generelt sett er det slik at vind fra sørøst og øst er gunstigere enn vind fra nord. Nordavind kan føre til at fisken blir mindre aktiv, da den kan føre med seg kaldere luft og redusere insektaktiviteten. Likevel er det ingen regel uten unntak, og vindforholdene kan variere fra vann til vann.
    # Documentation for wind direction: https://api.met.no/weatherapi/locationforecast/2.0/documentation

    # Wind from north not so good
    def wind_from_north(serie: Timeserie):
        return serie.data.instant.details.wind_from_direction < 90

    hours_north_wind = has_instant_condition(
        day_info, wind_from_north, "wind from north"
    )
    bad_conditions += hours_north_wind

    # Wind from east or southeast good
    def wind_from_southeast(serie: Timeserie):
        return (
            serie.data.instant.details.wind_from_direction > 90
            and serie.data.instant.details.wind_from_direction <= 180
        )

    hours_southeast_wind = has_instant_condition(
        day_info, wind_from_southeast, "wind from southeast"
    )
    good_conditions += hours_southeast_wind

    # Wind: no wind not good
    def no_wind(serie: Timeserie):
        return serie.data.instant.details.wind_speed <= 0.5

    hours_no_wind = has_instant_condition(day_info, no_wind, "no wind")
    bad_conditions += hours_no_wind

    # Wind: too much wind not good
    def to_much_wind(serie: Timeserie):
        return serie.data.instant.details.wind_speed >= 10

    hours_to_much_wind = has_instant_condition(day_info, to_much_wind, "too much wind")
    bad_conditions += hours_to_much_wind

    # Wind: a little windy good
    def ideal_wind(serie: Timeserie):
        return (
            serie.data.instant.details.wind_speed >= 1
            and serie.data.instant.details.wind_speed <= 5
        )

    hours_ideal_wind = has_instant_condition(day_info, ideal_wind, "ideal wind")
    good_conditions += hours_ideal_wind

    # Vann- og lufttemperatur: Ørreten trives best i kjøligere vann, ideelt mellom 10 og 15°C, men er fortsatt aktiv i vann opp til 20°C.
    # Good temp: Between 10-20
    def good_temperature(serie: Timeserie):
        return (
            serie.data.instant.details.air_temperature >= 10
            and serie.data.instant.details.air_temperature <= 20
        )

    hours_good_temperature = has_instant_condition(
        day_info, good_temperature, "good temperature"
    )
    good_conditions += hours_good_temperature

    # Bad temp: Outside of this range
    def bad_temperature(serie: Timeserie):
        return (
            serie.data.instant.details.air_temperature < 10
            and serie.data.instant.details.air_temperature > 20
        )

    hours_bad_temperature = has_instant_condition(
        day_info, bad_temperature, "bad temperature"
    )
    bad_conditions += hours_bad_temperature

    return good_conditions / bad_conditions
