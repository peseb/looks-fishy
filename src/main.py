from datetime import datetime, timedelta
from typing import Any, Iterable
from tabulate import tabulate
from get_fishing_location import get_fishing_location
from helper.calculate_fishing_conditions import calculate_fishing_conditions
from helper.color_condition_result import color_condition_result
from helper.get_condition_summary_text import get_condition_summary_text
from helper.is_data_for_date import is_data_for_date
from weather_forecast.get_weather_forecast import get_weather_forecast


def main():
    fishing_location = get_fishing_location()
    location_name = fishing_location.stedsnavn[0].skrivemåte
    print(f"Assessing conditions at {location_name}..\n\n")

    weather_forecast = get_weather_forecast(fishing_location)
    if weather_forecast is None:
        print("Uh-Oh, no weatherdata found. Unable to determine conditions ")
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
            f"{fishing_condition:.1f} ({get_condition_summary_text(fishing_condition)})"
        )
        print(f"\nFishing condition: {condition_str})")

        conditions.append(
            [
                current_date.date(),
                color_condition_result(fishing_condition, condition_str),
            ]
        )
        next_day = timedelta(days=1)
        current_date = current_date + next_day
        print("\n\n")

    print(f"Done! Here´s the forecast for {location_name}:")
    print(tabulate(conditions, headers=["Date", "Condition"]))


if __name__ == "__main__":
    main()
