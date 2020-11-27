import re
from typing import Iterator

import lxml.html
import requests
from base import LotSpaces, Scraper


class CharlotteScraper(Scraper):
    """Scrape Charlotte html.

    https://www.charlottecentercity.org/transportation/parking/
    """

    HTML_URL = "https://www.charlottecentercity.org/transportation/parking/"
    TIMEOUT = 5
    NAME_PATTERN = re.compile(r';results\[(\d+)\]\.name="(.*?)"')
    SPACES_PATTERN = re.compile(r';results\[(\d+)\]\.available="(\d+)"')
    CAPACITY_PATTERN = re.compile(r';results\[(\d+)\]\.capacity="(\d+)"')
    ADDRESS_PATTERN = re.compile(r';results\[(\d+)\]\.address="(.*?)"')

    name = "charlotte"

    def fetch_spaces(self) -> Iterator[LotSpaces]:
        response = requests.get(self.HTML_URL, timeout=self.TIMEOUT)
        response.raise_for_status()
        doc = lxml.html.fromstring(response.content)
        scripts = doc.xpath('//script[contains(text(), "var map")]')
        assert len(scripts) == 1
        script = scripts[0]

        names = dict(self.NAME_PATTERN.findall(script.text))
        spaces = dict(self.SPACES_PATTERN.findall(script.text))
        capacities = dict(self.CAPACITY_PATTERN.findall(script.text))
        addresses = dict(self.ADDRESS_PATTERN.findall(script.text))
        assert names.keys() == spaces.keys() == capacities.keys() == addresses.keys()

        seen = set()
        for key in names.keys():
            if names[key] in seen:
                continue
            seen.add(names[key])
            yield LotSpaces(
                lot=names[key],
                spaces=int(spaces[key]),
                capacity=int(capacities[key]),
                address=addresses[key],
            )
