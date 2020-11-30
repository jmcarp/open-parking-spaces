from typing import Iterator

import requests
from base import LotSpaces, Scraper


class NJITScraper(Scraper):
    """Scrape NJIT json.

    https://mobile.njit.edu/parking/
    """

    HOME_URL = "https://mobile.njit.edu/parking/"
    API_URL = "http://mobile.njit.edu/parking/data.php"
    TIMEOUT = 5

    name = "njit"

    def fetch_spaces(self) -> Iterator[LotSpaces]:
        session = requests.Session()
        session.get(self.HOME_URL, headers={"User-Agent": "open-parking-spaces"})
        response = session.post(
            self.API_URL, timeout=self.TIMEOUT, headers={"Referer": self.HOME_URL}
        )
        response.raise_for_status()
        data = response.json()
        for row in data["decks"].values():
            yield LotSpaces(
                lot=row["SiteName"],
                spaces=int(row["Available"]),
                capacity=int(row["Total"]),
                address=row["Address"],
            )
