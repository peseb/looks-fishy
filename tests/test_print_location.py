from src.helper.print_location import print_location
from src.location_search.search_result import Location, Municipality, Point, Stedsnavn


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

    res = print_location(loc)
    assert res == "Trondheim (Tettsted, 5001 Trondheim)"
