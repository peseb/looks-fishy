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
    result = (
        len(
            list(
                filter(
                    lambda x: check_condition(x),
                    day_info,
                )
            )
        )
        > 0
    )

    print(f"Has {condition_description}: {result}")
    return result


# Possible conditions can be found here: https://github.com/metno/weathericons/tree/main/weather
def calculate_fishing_conditions(day_info: List[Timeserie]):
    good_conditions = 1
    bad_conditions = 1

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

    # Wind: Vindretningen har stor påvirkning på ørretfiske. Generelt sett er det slik at vind fra sørøst og øst er gunstigere enn vind fra nord. Nordavind kan føre til at fisken blir mindre aktiv, da den kan føre med seg kaldere luft og redusere insektaktiviteten. Likevel er det ingen regel uten unntak, og vindforholdene kan variere fra vann til vann.
    # Documentation for wind direction: https://api.met.no/weatherapi/locationforecast/2.0/documentation
    def wind_from_north(serie: Timeserie):
        return serie.data.instant.details.wind_from_direction < 90

    def wind_from_southeast(serie: Timeserie):
        return (
            serie.data.instant.details.wind_from_direction > 90
            and serie.data.instant.details.wind_from_direction <= 180
        )

    has_north_wind = has_instant_condition(day_info, wind_from_north, "wind from north")
    has_southeast_wind = has_instant_condition(
        day_info, wind_from_southeast, "wind from southeast"
    )

    # Wind from north not so good
    if has_north_wind:
        bad_conditions += 1

    # Wind from east or southeast good
    if has_southeast_wind:
        good_conditions += 1

    # Wind: Vindstille: Kan gjøre det vanskeligere å fiske med flue eller sluk, da fisken lettere blir skremt av kast og uro
    # Vann- og lufttemperatur: Ørreten trives best i kjøligere vann, ideelt mellom 10 og 15°C, men er fortsatt aktiv i vann opp til 20°C.
    # Kjølige morgener eller kvelder, spesielt etter varme dager, kan gi gode forhold.
    # Tidspunkt på dagen:
    # Tidlig morgen og sen kveld er ofte de beste tidspunktene, da ørreten er mest aktiv i grålysningen og ved solnedgang, og ofte jakter nær overflaten.
    # På dagtid, når temperaturen er på sitt høyeste, kan ørreten være mer passiv og søke dypere vann.

    return good_conditions / bad_conditions
