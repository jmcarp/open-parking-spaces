import datetime
import logging

from google.cloud import bigquery
from scrapers.ann_arbor import AnnArborScraper
from scrapers.asheville import AshevilleScraper
from scrapers.birmingham import BirminghamScraper
from scrapers.madison import MadisonScraper
from scrapers.montgomery_county import MontgomeryCountyScraper
from scrapers.pittsburgh import PittsburghScraper
from scrapers.santa_barbara import SantaBarbaraScraper
from scrapers.union_city import UnionCityScraper
from scrapers.vail import VailScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCRAPER_CLASSES = [
    AnnArborScraper,
    AshevilleScraper,
    BirminghamScraper,
    MadisonScraper,
    MontgomeryCountyScraper,
    PittsburghScraper,
    SantaBarbaraScraper,
    UnionCityScraper,
    VailScraper,
]

TABLE_PATH = "open-parking-spaces.spaces.lot_spaces"


def scrape(event, context):
    bq_client = bigquery.Client()
    timestamp = datetime.datetime.utcnow()
    errors = []
    for scraper_class in SCRAPER_CLASSES:
        logger.info(f"Processing scraper class {scraper_class}")
        scraper = scraper_class()
        try:
            scraper.scrape(bq_client, TABLE_PATH, timestamp)
        except Exception as error:
            logger.exception(error)
            errors.append(error)
    if len(errors) > 0:
        raise ValueError(errors)


if __name__ == "__main__":
    scrape({}, {})
