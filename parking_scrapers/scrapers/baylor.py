import json
import re
from typing import Iterator

import requests
from base import LotSpaces, Scraper


class BaylorScraper(Scraper):
    """Scrape Baylor json.

    https://www.baylor.edu/dps/index.php?id=973615
    """

    API_URL = "https://streetsoncloud.com/parking/rest/occupancymap/id/160"
    TIMEOUT = 5
    JSON_PATTERN = re.compile(rb"^callback\((.*?)\)$", re.IGNORECASE)

    name = "baylor"

    def fetch_spaces(self) -> Iterator[LotSpaces]:
        response = requests.get(self.API_URL, timeout=self.TIMEOUT)
        response.raise_for_status()
        match = self.JSON_PATTERN.search(response.content)
        assert match is not None
        data = json.loads(match.groups()[0])
        for result in data["results"]:
            for row in result.values():
                yield LotSpaces(
                    lot=row["location_name"],
                    spaces=int(row["free_spaces"]),
                    capacity=int(row["total_spaces"]),
                )
