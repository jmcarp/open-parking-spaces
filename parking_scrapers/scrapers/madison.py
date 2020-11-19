from typing import Iterator

import requests
from base import LotSpaces, Scraper


class MadisonScraper(Scraper):
    API_URL = (
        "https://www.cityofmadison.com/parking-utility/data/ramp-availability.json"
    )
    TIMEOUT = 5

    name = "madison"

    def fetch_spaces(self) -> Iterator[LotSpaces]:
        response = requests.get(self.API_URL, timeout=self.TIMEOUT)
        response.raise_for_status()
        data = response.json()
        for row in data:
            yield LotSpaces(
                lot=row["name"],
                spaces=row["vacant_stalls"],
                id=str(row["id"]),
                url=row["url"],
            )
