import re
from typing import Iterator

import lxml.html
import requests
from base import LotSpaces, Scraper


class CharlottesvilleScraper(Scraper):
    """Scrape Charlottesville html.

    https://www.charlottesville.gov/240/Parking-Garages
    """

    HTML_URL = "https://widget.charlottesville.org/parkingcounter/parkinglot"
    TIMEOUT = 5
    LOTS = {
        "market": "Market Street Garage",
        "water": "Water Street Garage",
    }
    IMAGE_PATTERN = re.compile(r"images/([b\d])[a-z]\.gif", re.IGNORECASE)

    name = "charlottesville"

    def fetch_spaces(self) -> Iterator[LotSpaces]:
        for lot_id, lot_name in self.LOTS.items():
            url = f"{self.HTML_URL}?lotname={lot_id}"
            response = requests.get(url, timeout=self.TIMEOUT)
            response.raise_for_status()
            doc = lxml.html.fromstring(response.content)

            digits = [
                self.image_to_digit(image)
                for image in doc.xpath("//div[@id='divAvailableSpaces']/img/@src")
            ]
            while digits and digits[0] == "b":
                digits = digits[1:]
            assert len(digits) > 0
            spaces = int("".join(digits))

            yield LotSpaces(
                lot=lot_name,
                spaces=spaces,
            )

    def image_to_digit(self, url: str) -> str:
        match = self.IMAGE_PATTERN.search(url)
        assert match is not None
        return match.groups()[0]
