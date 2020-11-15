import re
from typing import Iterator

import lxml.html
import requests
from base import LotSpaces, Scraper


class PittsburghScraper(Scraper):
    HTML_URL = "https://parkpgh.org/"
    SPACES_PATTERN = re.compile(r"(\d+)\sspots\savailable", re.IGNORECASE)
    FULL_MESSAGE = "Lot is full or few spaces available"

    name = "pittsburgh"

    def fetch_spaces(self) -> Iterator[LotSpaces]:
        response = requests.get(
            self.HTML_URL, headers={"User-Agent": "open-parking-spaces"}
        )
        response.raise_for_status()
        doc = lxml.html.fromstring(response.content)
        divs = doc.xpath("//div[@id='garage-list']/div[contains(@class, 'list-item')]")
        for div in divs:
            lot = div.xpath(".//h1/text()")[0]
            available = div.xpath(".//p[contains(@class, 'available')]/text()")[0]
            if available == self.FULL_MESSAGE:
                spaces = "0"
            else:
                match = self.SPACES_PATTERN.search(available)
                assert match is not None
                (spaces,) = match.groups()
            yield LotSpaces(
                lot=lot,
                spaces=int(spaces),
            )
