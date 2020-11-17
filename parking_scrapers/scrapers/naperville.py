from typing import Iterator

import lxml.html
import requests
from base import LotSpaces, Scraper


class NapervilleScraper(Scraper):
    HTML_URL = "https://www.naperville.il.us/about-naperville/transportation-and-parking/downtown-parking/"  # noqa: E501

    name = "naperville"

    def fetch_spaces(self) -> Iterator[LotSpaces]:
        response = requests.get(self.HTML_URL)
        response.raise_for_status()
        doc = lxml.html.fromstring(response.content)
        sections = doc.xpath(
            '//div[contains(@class, "parking-spaces")]'
            '//div[contains(@class, "section")]'
        )
        for section in sections:
            section_title = section.xpath(".//h3/text()")[0]
            rows = section.xpath('.//div[contains(@class, "row")]')
            for row in rows:
                location_title = row.xpath(
                    './/*[contains(@class, "location-title")]/text()'
                )[0]
                spaces = (
                    row.xpath('.//div[contains(@class, "spaces-available")]')[0]
                    .text_content()
                    .strip()
                )
                lot = f"{section_title}: {location_title}"
                yield LotSpaces(
                    lot=lot, spaces=int(spaces) if "full" not in spaces.lower() else 0
                )
