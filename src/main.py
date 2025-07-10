from src.search.search import search_for_location


fishing_location = None
while fishing_location is None:
    user_input = input("Enter a location: ")

    print(f"Searching for location: {user_input}")
    search_result = search_for_location(user_input)
    if search_result is None or search_result.metadata.totaltAntallTreff == 0:
        print("Unable to find location.. Try again")
        continue

    total_hits = search_result.metadata.totaltAntallTreff
    if total_hits > 1:
        print("Found multiple locations. Select one from the list: ")
        for index, res in enumerate(search_result):
            print(f"{index + 1}. {res}")

        selected_index = int(input("Enter the number matching your location"))
        while selected_index < 0 or selected_index > total_hits:
            selected_index = int(
                input(f"Invalid choice. Enter a number between {1}-{total_hits}.")
            )
        fishing_location = search_result.navn[selected_index - 1]
    else:
        fishing_location = search_result.navn[0]

# Location has been found
print(f"Assessing conditions at {fishing_location}..")
# TODO: Calculate fishing conditions
# TODO: Print result for user
