from typing import Optional
import requests

from search.search_result import SearchResponse


def search_for_location(search_string: str) -> Optional[SearchResponse]:
    url = f"https://api.kartverket.no/stedsnavn/v1/sted?sok={search_string}&fuzzy=true&utkoordsys=4258&treffPerSide=10&side=1"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return SearchResponse(**data)
    except Exception as e:
        print(f"Error during API request: {e}")
        return None
