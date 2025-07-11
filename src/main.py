from datetime import datetime, timedelta
import time
from get_fishing_location import get_fishing_location
from helper.is_data_for_date import is_data_for_date
from weather_forecast.get_weather_forecast import get_weather_forecast


def main():
    fishing_location = get_fishing_location()
    print(f"Assessing conditions at {fishing_location}..")

    weather_forecast = get_weather_forecast(fishing_location)
    if weather_forecast is None:
        print("UhOh, no weatherdata found. Unable to determine conditions ")
        return

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
        # TODO: Calculate fishing conditions
        # TODO: Print result for user

        # Move to next day
        next_day = timedelta(days=1)
        current_date = current_date + next_day
        time.sleep(1)

    print("Done!")


if __name__ == "__main__":
    main()
