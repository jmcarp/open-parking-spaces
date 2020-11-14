from typing import Iterator

import requests
from base import LotSpaces, Scraper


class SantaBarbaraScraper(Scraper):
    API_URL = "https://www.santabarbaraca.gov/civicax/parking/api/status/"

    name = "santa_barbara"

    def fetch_spaces(self) -> Iterator[LotSpaces]:
        response = requests.get(self.API_URL)
        response.raise_for_status()
        data = response.json()
        for row in data:
            # This lot shows a capacity of 9999 and doesn't appear on the website
            if row["CarparkName"] == "Lot 9-3 Base":
                continue
            yield LotSpaces(
                lot=row["CarparkName"],
                spaces=row["Capacity"] - row["CurrentLevel"],
                capacity=row["Capacity"],
                id=str(row["CarparkNo"]),
            )
