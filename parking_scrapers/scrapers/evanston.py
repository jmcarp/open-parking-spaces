import re
from typing import Iterator

import requests
from base import LotSpaces, Scraper


class EvanstonScraper(Scraper):
    """Scrape smarking api for Evanston.

    Get garage ids and api key from
    https://widgets.smarking.com/city-of-evanston/index.html
    """

    METADATA_API_URL = "https://my.smarking.net/api/users/v1/garages/id/{}"
    OCCUPANCY_API_URL = "https://my.smarking.com/api/ds/v3/garages/{}/current/occupancy"
    API_KEY = "a0OrkKhPK3vRtDFCLnbCibc7G5_LHSgU2V-4jufR"
    TIMEOUT = 5
    GARAGE_IDS = [292744, 184215, 835525]
    NAME_PREFIX_PATTERN = re.compile(r"^\*Evanston - ", re.IGNORECASE)

    name = "evanston"

    def fetch_spaces(self) -> Iterator[LotSpaces]:
        for garage_id in self.GARAGE_IDS:
            metadata_response = requests.get(
                self.METADATA_API_URL.format(garage_id),
                headers={"Authorization": f"Bearer {self.API_KEY}"},
                timeout=self.TIMEOUT,
            )
            metadata_response.raise_for_status()
            metadata_data = metadata_response.json()

            occupancy_response = requests.get(
                self.OCCUPANCY_API_URL.format(garage_id),
                headers={"Authorization": f"Bearer {self.API_KEY}"},
                timeout=self.TIMEOUT,
            )
            occupancy_response.raise_for_status()
            occupancy_data = occupancy_response.json()
            occupancy_rows = occupancy_data["value"]
            assert len(occupancy_rows) <= 1
            total_occupancy = next(
                (row for row in occupancy_rows if row["group"] == "Total"), None
            )
            occupancy = total_occupancy["value"] if total_occupancy is not None else 0

            lot = self.NAME_PREFIX_PATTERN.sub("", metadata_data["name"])

            yield LotSpaces(
                lot=lot,
                spaces=metadata_data["spaces"] - occupancy,
                capacity=metadata_data["spaces"],
                id=str(metadata_data["id"]),
                address=metadata_data["address1"],
            )
