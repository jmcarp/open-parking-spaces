from typing import Iterator

import lxml.html
import requests
from base import LotSpaces, Scraper


class TAMUScraper(Scraper):
    HTML_URL = "https://transport.tamu.edu/parking/realtime.aspx"
    TIMEOUT = 5

    name = "tamu"

    def fetch_spaces(self) -> Iterator[LotSpaces]:
        response = requests.get(self.HTML_URL, timeout=self.TIMEOUT)
        response.raise_for_status()
        doc = lxml.html.fromstring(response.content)
        for td in doc.xpath('//td[contains(@class, "garage")]'):
            lot = td.xpath('./span[contains(@class, "small")]/text()')[0]
            spaces = int(td.xpath('../td[contains(@class, "count")]/span/text()')[0])
            url = td.xpath("./a/@href")[0]
            yield LotSpaces(
                lot=lot,
                spaces=spaces,
                url=url,
            )
