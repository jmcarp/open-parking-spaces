from typing import Iterator

import requests
from base import LotSpaces, Scraper


class LagunaBeachScraper(Scraper):
    """Scrape Laguna Beach json.

    https://app.lagunabeachparking.net/
    """

    API_URL = "https://dataservices.frogparking.com/FrogParkingService.svc/GetPublicParkingLocations"  # noqa: E501
    TIMEOUT = 5

    name = "laguna_beach"

    def fetch_spaces(self) -> Iterator[LotSpaces]:
        response = requests.post(
            self.API_URL,
            timeout=self.TIMEOUT,
            json={
                "OrganizationId": "86999b40-7810-4174-b1d0-42a2bb55f165",
                "IncludeLevels": True,
            },
        )
        response.raise_for_status()
        data = response.json()
        for row in data["PublicParkingLocations"]:
            levels = row["LocationLevels"]
            assert len(levels) == 1
            level = levels[0]
            yield LotSpaces(
                lot=row["Name"],
                spaces=level["VacantBays"],
                capacity=level["TotalBays"],
                id=row["Id"],
            )
