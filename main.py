from helper.search import search_for_location


fishing_location = None

while (fishing_location is None):
    user_input = input("Enter a location: ")
    print(f"Searching for location: {user_input}")

    search_result = search_for_location(user_input)
    if (len(search_result) == 0):
        print("Unable to find location.. Try again.")
        continue

    if (len(search_result) > 1):
        print("Found multiple locations. Select one from the list: ")
        for index, res in enumerate(search_result):
            print(f"{index}. {res}")
        selected = None
        selected_index = input("Enter the number matching your location")
        # TODO: Valudate index..
        fishing_location = search_result[int(selected_index)]
    else:
        fishing_location = search_result[0]

# Location has been found
print(f"Assessing conditions at {fishing_location}..")


            
