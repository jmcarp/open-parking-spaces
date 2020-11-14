import re
from typing import Iterator

import lxml.html
import requests
from base import LotSpaces, Scraper


class VailScraper(Scraper):
    HTML_URL = "http://www.vailassets.com/ParkingCounts/tabid/131/Default.aspx"
    SPACES_PATTERN = re.compile(r"(\d+) spaces of (\d+) open", re.IGNORECASE)

    name = "vail"

    def fetch_spaces(self) -> Iterator[LotSpaces]:
        response = requests.get(self.HTML_URL)
        response.raise_for_status()
        doc = lxml.html.fromstring(response.content)
        divs = doc.xpath("//h4/parent::div")
        for div in divs:
            texts = div.xpath(".//text()")
            lot = texts[0].split(" - ")[0]
            spaces, capacity = None, None
            for text in texts:
                match = self.SPACES_PATTERN.search(text)
                if match is not None:
                    spaces, capacity = match.groups()
                    break
            yield LotSpaces(
                lot=lot,
                spaces=int(spaces),
                capacity=int(capacity),
            )
