from get_fishing_location import get_fishing_location
from weather_forecast.get_weather_forecast import get_weather_forecast


def main():
    fishing_location = get_fishing_location()
    print(f"Assessing conditions at {fishing_location}..")

    weather_forecast = get_weather_forecast(fishing_location)
    print("Weather forecast: ", weather_forecast)
    # TODO: Calculate fishing conditions
    # TODO: Print result for user


if __name__ == "__main__":
    main()
