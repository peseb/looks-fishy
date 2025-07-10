from location_search.search_result import Location


def print_location(location: Location):
    place = location.stedsnavn[0]
    municipality = location.kommuner[0]
    return f"{place.skrivemåte} ({location.navneobjekttype}, {municipality.kommunenummer} {municipality.kommunenavn})"
