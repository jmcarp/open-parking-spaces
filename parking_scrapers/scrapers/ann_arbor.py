import re
from typing import Iterator

import lxml.html
import requests
from base import LotSpaces, Scraper


class AnnArborScraper(Scraper):
    HTML_URL = "https://payment.rpsa2.com/LocationAndRate/SpaceAvailability"
    SPACES_PATTERN = re.compile(r"(.*?) - (\d+) spaces as of at ([\w\s\.]+)")
    ADDRESS_OVERRIDES = {"305 S. Ashley": "305 S. Ashley St."}

    name = "ann_arbor"

    def fetch_spaces(self) -> Iterator[LotSpaces]:
        response = requests.get(self.HTML_URL)
        response.raise_for_status()
        doc = lxml.html.fromstring(response.content)
        for td in doc.xpath("//a[contains(@href, 'geo:')]/.."):
            for script in td.xpath("script"):
                script.drop_tree()
            text = re.sub(r"\s+", " ", td.text_content().strip())
            match = self.SPACES_PATTERN.search(text)
            if match is None:
                continue
            lot, spaces, address = match.groups()
            address = self.ADDRESS_OVERRIDES.get(address, address)
            yield LotSpaces(
                lot=lot.strip(),
                spaces=int(spaces),
                address=address,
            )
