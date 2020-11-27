import re
from typing import Iterator

import requests
from base import LotSpaces, Scraper


class WalnutCreekScraper(Scraper):
    """Scrape smarking api for Walnut Creek.

    Get garage ids and api key from
    https://widgets.smarking.com/walnut-creek-map/index.html
    """

    GEODATA_API_URL = "https://my.smarking.net/api/map/v1/garages/{}/geo-data"
    OCCUPANCY_API_URL = (
        "https://my.smarking.net/api/ds/v3/garages/{}/current/occupancy?gb=Map"
    )
    API_KEY = "mOmJ3a19zzhCrGg3P0pFwt_izM3mjkdJDDlOv-Rj"
    TIMEOUT = 5
    LOCATION_ID = 396811
    LOT_NAMES = [
        "Broadway Garage",
        "Lesher Center Garage",
        "South Locust Garage",
    ]
    NAME_PREFIX_PATTERN = re.compile(r"^\d+ - ")

    name = "walnut_creek"

    def fetch_spaces(self) -> Iterator[LotSpaces]:
        geo_response = requests.get(
            self.GEODATA_API_URL.format(self.LOCATION_ID),
            headers={"Authorization": f"Bearer {self.API_KEY}"},
            timeout=self.TIMEOUT,
        )
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        occupancy_response = requests.get(
            self.OCCUPANCY_API_URL.format(self.LOCATION_ID),
            headers={"Authorization": f"Bearer {self.API_KEY}"},
            timeout=self.TIMEOUT,
        )
        occupancy_response.raise_for_status()
        occupancy_data = occupancy_response.json()

        for lot in self.LOT_NAMES:
            geo_row = next(
                row for row in geo_data["value"]["areas"] if row["areaId"] == lot
            )
            occupancy_row = next(
                row for row in occupancy_data["value"] if row["group"] == lot
            )
            yield LotSpaces(
                lot=lot,
                spaces=geo_row["spaces"] - occupancy_row["value"],
                capacity=geo_row["spaces"],
            )
