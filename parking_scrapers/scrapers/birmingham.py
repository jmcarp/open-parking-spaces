from typing import Iterator

import lxml.html
import requests
from base import LotSpaces, Scraper


class BirminghamScraper(Scraper):
    """Scrape Birmingham, MI html and json.

    https://www.bhamgov.org/
    """

    HTML_URL = "https://www.bhamgov.org"
    JSON_URL = "https://cms.revize.com/revize/apps/birminghamparking/index.php"
    TIMEOUT = 5

    name = "birmingham"

    def fetch_spaces(self) -> Iterator[LotSpaces]:
        html_response = requests.get(self.HTML_URL, timeout=self.TIMEOUT)
        html_response.raise_for_status()
        doc = lxml.html.fromstring(html_response.content)
        rows = doc.xpath(
            '//div[@id="parking-widget"]//a[contains(@class, "widget-row")]'
        )
        id_to_name = {}
        for row in rows:
            lot_name = row.xpath('.//div[contains(@class, "left-col")]/text()')[
                0
            ].strip()
            lot_id = row.xpath('.//div[contains(@class, "count")]/@data-parking-id')[0]
            id_to_name[lot_id] = lot_name

        json_response = requests.get(self.JSON_URL, timeout=self.TIMEOUT)
        json_response.raise_for_status()
        json_data = json_response.json()
        for lot_id, spaces in json_data.items():
            yield LotSpaces(
                lot=id_to_name[lot_id],
                spaces=spaces,
                id=lot_id,
            )
