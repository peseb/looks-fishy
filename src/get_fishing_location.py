from helper.format_location import format_location
from location_search.search import search_for_location
from location_search.search_result import Location


def get_fishing_location() -> Location:
    user_input = input("Enter a location: ")

    print(f"Searching for location: {user_input}")
    search_result = search_for_location(user_input)
    if search_result is None or search_result.metadata.totaltAntallTreff == 0:
        print("Unable to find location.. Try again")
        return get_fishing_location()

    total_hits = search_result.metadata.totaltAntallTreff
    if total_hits > 1:
        print("Found multiple locations. Select one from the list: \n")
        for index, location in enumerate(search_result.navn):
            print(f"{index + 1}. {format_location(location)}")

        selected_index = int(input("\nEnter the number matching your location: "))
        while selected_index < 0 or selected_index > total_hits:
            selected_index = int(
                input(f"Invalid choice. Enter a number between {1}-{total_hits}.")
            )
        return search_result.navn[selected_index - 1]
    else:
        return search_result.navn[0]
