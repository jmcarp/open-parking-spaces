from typing import Iterator

import requests
from base import LotSpaces, Scraper


class MontgomeryCountyScraper(Scraper):
    """Scrape Montgomery County api.

    https://data.montgomerycountymd.gov/Transportation/Parking-Garage-Space-Availability/qahs-fevu
    """

    API_URL = "https://data.montgomerycountymd.gov/resource/qahs-fevu.json"
    GARAGE_NAMES = {
        "GAR 31": "Capital Crescent Garage",
        "GAR 57": "Elm Garage",
        "GAR 60": "Wayne Avenue Garage",
        "GAR 61": "Town Square Garage",
    }

    name = "montgomery_county"

    def fetch_spaces(self) -> Iterator[LotSpaces]:
        response = requests.get(self.API_URL)
        response.raise_for_status()
        data = response.json()
        for row in data:
            facility = row["facilitynumber"]
            spaces = int(row["space_count"])
            capacity = int(row["total_spaces"])
            yield LotSpaces(
                lot=self.GARAGE_NAMES.get(facility, facility),
                spaces=int(spaces),
                capacity=int(capacity),
            )
