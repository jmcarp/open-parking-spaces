import abc
import datetime
from dataclasses import asdict, dataclass
from typing import Iterator, Optional

from google.cloud import bigquery


@dataclass
class LotSpaces:
    lot: str
    spaces: int
    capacity: Optional[int] = None
    id: Optional[str] = None
    url: Optional[str] = None
    address: Optional[str] = None


class Scraper(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fetch_spaces(self) -> Iterator[LotSpaces]:
        pass

    @abc.abstractproperty
    def name(self) -> str:
        pass

    def scrape(
        self, bq_client: bigquery.Client, table_path: str, timestamp: datetime.datetime
    ):
        table = bq_client.get_table(table_path)
        rows = [
            {
                "provider": self.name,
                "timestamp": timestamp,
                **asdict(row),
            }
            for row in self.fetch_spaces()
        ]
        errors = bq_client.insert_rows(table, rows)
        if len(errors) > 0:
            raise ValueError(errors)
