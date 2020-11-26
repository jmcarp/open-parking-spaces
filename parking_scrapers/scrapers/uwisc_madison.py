import re
from typing import Iterator

import requests
from base import LotSpaces, Scraper


class UWisconsinMadisonScraper(Scraper):
    API_URL = "https://gates.transportation.wisc.edu/occupancy/"
    TIMEOUT = 5
    SPACES_PATTERN = re.compile(r"\s+")

    name = "uwisc_madison"

    def fetch_spaces(self) -> Iterator[LotSpaces]:
        response = requests.get(self.API_URL, timeout=self.TIMEOUT)
        response.raise_for_status()
        data = response.json()
        for _, lots in data.items():
            if not isinstance(lots, dict):
                continue
            for lot, attributes in lots.items():
                yield LotSpaces(
                    lot=self.SPACES_PATTERN.sub(" ", lot),
                    spaces=attributes["vacancies"],
                )
