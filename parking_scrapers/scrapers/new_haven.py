import re
from typing import Iterator

import lxml.html
import requests
from base import LotSpaces, Scraper


class NewHavenScraper(Scraper):
    """Scrape New Haven html.

    https://parknewhaven.com
    """

    HTML_URL = "https://parknewhaven.com"
    SPACES_PATTERN = re.compile(r"(.*?):\s+(\d+)% \((\d+) available\)", re.IGNORECASE)

    name = "new_haven"

    def fetch_spaces(self) -> Iterator[LotSpaces]:
        response = requests.get(
            self.HTML_URL, headers={"User-Agent": "open-parking-spaces"}
        )
        response.raise_for_status()
        doc = lxml.html.fromstring(response.content)
        links = doc.xpath(
            '//div[contains(@class, "tickr")]//a[contains(@class, "tickrlink")]'
        )
        for link in links:
            match = self.SPACES_PATTERN.search(link.text_content())
            assert match is not None
            lot, percent, spaces = match.groups()
            yield LotSpaces(
                lot=lot,
                spaces=int(spaces),
                url=link.attrib["href"],
            )
