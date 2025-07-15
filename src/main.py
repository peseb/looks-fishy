from datetime import datetime, timedelta
from typing import Any, Iterable

from colorama import Fore, Style
from tabulate import tabulate
from get_fishing_location import get_fishing_location
from helper.calculate_fishing_conditions import calculate_fishing_conditions
from helper.is_data_for_date import is_data_for_date
from weather_forecast.get_weather_forecast import get_weather_forecast


def color_condition(condition: float, condition_str: str) -> str:
    if condition < 1:
        return Fore.RED + condition_str + Style.RESET_ALL
    elif condition < 2:
        return Fore.YELLOW + condition_str + Style.RESET_ALL
    elif condition < 3:
        return Fore.LIGHTGREEN_EX + condition_str + Style.RESET_ALL

    return Fore.GREEN + condition_str + Style.RESET_ALL


def get_condition_summary(fishing_condition: float) -> str:
    if fishing_condition < 1:
        return "Bad"
    elif fishing_condition < 2:
        return "Decent"
    elif fishing_condition < 3:
        return "Good"

    return "Excellent"


def main():
    fishing_location = get_fishing_location()
    print(f"Assessing conditions at {fishing_location}..")

    weather_forecast = get_weather_forecast(fishing_location)
    if weather_forecast is None:
        print("UhOh, no weatherdata found. Unable to determine conditions ")
        return
    conditions: Iterable[Iterable[Any]] = []
    current_date = datetime.now()
    while True:
        day_info = list(
            filter(
                lambda x: is_data_for_date(x.time, current_date),
                weather_forecast.properties.timeseries,
            )
        )
        if len(day_info) == 0:
            break

        print(
            "*********************************************************************************"
        )
        print(f"Date: {current_date.date()}")
        fishing_condition = calculate_fishing_conditions(day_info)
        condition_str = (
            f"{fishing_condition:.1f} ({get_condition_summary(fishing_condition)})"
        )
        print(f"\nFishing condition: {condition_str})")

        conditions.append(
            [current_date.date(), color_condition(fishing_condition, condition_str)]
        )
        next_day = timedelta(days=1)
        current_date = current_date + next_day
        print("\n\n")

    print("Done! Here's a summary:")
    print(tabulate(conditions, headers=["Date", "Condition"]))


if __name__ == "__main__":
    main()
