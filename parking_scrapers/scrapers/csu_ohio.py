from typing import Iterator

import requests
from base import LotSpaces, Scraper


class CSUOhioScraper(Scraper):
    """Scrape CSU Ohio json.

    http://parkingspaces.csuohio.edu/
    """

    API_URL = "http://parkingspaces.csuohio.edu/feed.php"
    TIMEOUT = 5
    SKIP_LOTS = {"Total of All Garages"}

    name = "csu_ohio"

    def fetch_spaces(self) -> Iterator[LotSpaces]:
        response = requests.get(self.API_URL, timeout=self.TIMEOUT)
        response.raise_for_status()
        data = response.json()
        for row in data:
            if row["name"] in self.SKIP_LOTS:
                continue
            yield LotSpaces(
                lot=row["name"],
                spaces=int(row["SubscriberCapacity"]) - int(row["SubscriberCount"]),
                capacity=int(row["SubscriberCapacity"]),
                id=str(row["LotId"]),
            )
