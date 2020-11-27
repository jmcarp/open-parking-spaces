from typing import Iterator

import requests
from base import LotSpaces, Scraper


class AuburnScraper(Scraper):
    """Scrape Auburn, AL json.

    https://webgis.auburnalabama.org/cityofauburnparking/
    Logic adapted from https://webgis.auburnalabama.org/cityofauburnparking/Scripts/gisScript.js.
    """  # noqa: E501

    API_URL = "https://api2.auburnalabama.org/parking/enforcement/old"
    TIMEOUT = 5

    name = "auburn"

    def fetch_spaces(self) -> Iterator[LotSpaces]:
        response = requests.get(self.API_URL, timeout=self.TIMEOUT)
        response.raise_for_status()
        data = response.json()
        counts = {
            "Parking Deck": {"spaces": 0, "capacity": 0},
            "Gay St Lot": {"spaces": 0, "capacity": 0},
        }
        for row in data:
            if row["StallType"] is not None:
                if 100 <= row["StallNumber"] < 200:
                    counts["Parking Deck"]["capacity"] += 1
                    if not row["Occupied"]:
                        counts["Parking Deck"]["spaces"] += 1
                elif row["StallNumber"] < 100:
                    counts["Gay St Lot"]["capacity"] += 1
                    if not row["Occupied"]:
                        counts["Gay St Lot"]["spaces"] += 1
        for lot, details in counts.items():
            yield LotSpaces(
                lot=lot, spaces=details["spaces"], capacity=details["capacity"]
            )
