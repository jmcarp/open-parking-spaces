import re
from typing import Iterator

import requests
from base import LotSpaces, Scraper


class UnionCityScraper(Scraper):
    """Scrape smarking api for Union City.

    Get garage ids and api key from
    https://widgets.smarking.com/union-city-realtime-occupancy/index.html
    """

    API_URL = "https://my.smarking.net/api/users/v1/garages/id"
    API_KEY = "IPljSUq_qhbN8Ycz6bCpl29LOHt0yzii77ybc_-w"
    GARAGE_IDS = [929459, 250469, 908408, 634190, 323000, 174384, 252149, 949442]
    NAME_PREFIX_PATTERN = re.compile(r"^\d+ - ")

    name = "union_city"

    def fetch_spaces(self) -> Iterator[LotSpaces]:
        for garage_id in self.GARAGE_IDS:
            response = requests.get(
                f"{self.API_URL}/{garage_id}",
                headers={"Authorization": f"Bearer {self.API_KEY}"},
            )
            response.raise_for_status()
            data = response.json()
            lot = self.NAME_PREFIX_PATTERN.sub("", data["name"])
            yield LotSpaces(
                lot=lot,
                spaces=data["spaces"],
                id=str(data["id"]),
                address=data["address1"],
            )
