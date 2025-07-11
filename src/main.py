from datetime import datetime, timedelta
from get_fishing_location import get_fishing_location
from weather_forecast.get_weather_forecast import get_weather_forecast
from weather_forecast.weather_response import Timeserie


def is_data_for_date(timeserie: Timeserie, date: datetime):
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    timeserie_date = datetime.strptime(timeserie.time, date_format)
    return timeserie_date.date() == date.date()


def main():
    fishing_location = get_fishing_location()
    print(f"Assessing conditions at {fishing_location}..")

    weather_forecast = get_weather_forecast(fishing_location)
    if weather_forecast is None:
        print("UhOh, no weatherdata found. Unable to determine conditions ")
        return

    print("Weather forecast: ", weather_forecast)
    current_date = datetime.now()
    while True:
        day_info = list(
            filter(
                lambda x: is_data_for_date(x, current_date),
                weather_forecast.properties.timeseries,
            )
        )
        if len(day_info) == 0:
            break

        print("Assessing date: ", current_date)
        # TODO: Calculate fishing conditions
        # TODO: Print result for user

        # Move to next day
        next_day = timedelta(days=1)
        current_date = current_date + next_day

    print("Done!")


if __name__ == "__main__":
    main()
