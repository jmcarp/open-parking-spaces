import re
from typing import Iterator

import requests
from base import LotSpaces, Scraper


class SFMTAScraper(Scraper):
    API_URL = "https://services.sfmta.com/arcgis/rest/services/Parking/sfpark_ODS/MapServer/3/query"  # noqa: E501
    API_PARAMS = {
        "f": "json",
        "resultOffset": "0",
        "resultRecordCount": "1000",
        "where": "1=1",
        "outFields": "*",
        "outSR": "102100",
        "spatialRel": "esriSpatialRelIntersects",
    }
    TIMEOUT = 5
    # Skip lot with capacity 9999
    # See https://twitter.com/whatthecarp/status/1328926510573645824
    SKIP_LOTS = {"Mission Bartlett Garage"}
    SPACES_PATTERN = re.compile(
        r"estimated (\d+) of (\d+) spaces available", re.IGNORECASE
    )

    name = "sfmta"

    def fetch_spaces(self) -> Iterator[LotSpaces]:
        response = requests.get(
            self.API_URL, params=self.API_PARAMS, timeout=self.TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
        for feature in data["features"]:
            lot = feature["attributes"]["NAME"]
            if lot in self.SKIP_LOTS:
                continue
            match = self.SPACES_PATTERN.search(feature["attributes"]["AVAIL_MSG"])
            if match is not None:
                spaces, capacity = match.groups()
                yield LotSpaces(
                    lot=lot,
                    spaces=int(spaces),
                    capacity=int(capacity),
                    id=feature["attributes"]["OSP_ID"],
                    address=feature["attributes"]["ADDRESS"],
                )
