from typing import Iterator

import requests
from base import LotSpaces, Scraper


class AshevilleScraper(Scraper):
    API_URLS = [
        "https://s3.amazonaws.com/asheville-parking-decks/spaces.json",
        "https://s3.amazonaws.com/bc-parking-decks/164College",
        "https://s3.amazonaws.com/bc-parking-decks/40Coxe",
    ]

    name = "asheville"

    def fetch_spaces(self) -> Iterator[LotSpaces]:
        for api_url in self.API_URLS:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            for deck in data["decks"]:
                yield LotSpaces(
                    lot=deck["name"],
                    spaces=int(deck["available"]),
                )
