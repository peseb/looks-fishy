from helper.format_location import format_location
from location_search.search_result import Location, Municipality, Point, Stedsnavn


def test_print_location():
    pnkt = Point(nord=60, øst=10)
    municipality = Municipality(kommunenavn="Trondheim", kommunenummer="5001")
    place = Stedsnavn(skrivemåte="Trondheim")
    loc = Location(
        representasjonspunkt=pnkt,
        navneobjekttype="Tettsted",
        kommuner=[municipality],
        stedsnavn=[place],
    )

    formatted = format_location(loc)
    assert formatted == "Trondheim (Tettsted, 5001 Trondheim)"
