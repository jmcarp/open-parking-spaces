import datetime
import logging

from google.cloud import bigquery
from scrapers.ann_arbor import AnnArborScraper
from scrapers.asheville import AshevilleScraper
from scrapers.auburn import AuburnScraper
from scrapers.baylor import BaylorScraper
from scrapers.birmingham import BirminghamScraper
from scrapers.charlotte import CharlotteScraper
from scrapers.charlottesville import CharlottesvilleScraper
from scrapers.csu_ohio import CSUOhioScraper
from scrapers.evanston import EvanstonScraper
from scrapers.laguna_beach import LagunaBeachScraper
from scrapers.madison import MadisonScraper
from scrapers.montgomery_county import MontgomeryCountyScraper
from scrapers.naperville import NapervilleScraper
from scrapers.new_haven import NewHavenScraper
from scrapers.njit import NJITScraper
from scrapers.pittsburgh import PittsburghScraper
from scrapers.santa_barbara import SantaBarbaraScraper
from scrapers.sfmta import SFMTAScraper
from scrapers.union_city import UnionCityScraper
from scrapers.uwisc_madison import UWisconsinMadisonScraper
from scrapers.vail import VailScraper
from scrapers.walnut_creek import WalnutCreekScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCRAPER_CLASSES = [
    AnnArborScraper,
    AshevilleScraper,
    AuburnScraper,
    BaylorScraper,
    BirminghamScraper,
    CharlotteScraper,
    CharlottesvilleScraper,
    CSUOhioScraper,
    EvanstonScraper,
    LagunaBeachScraper,
    MadisonScraper,
    MontgomeryCountyScraper,
    NapervilleScraper,
    NewHavenScraper,
    NJITScraper,
    PittsburghScraper,
    SantaBarbaraScraper,
    SFMTAScraper,
    UnionCityScraper,
    UWisconsinMadisonScraper,
    VailScraper,
    WalnutCreekScraper,
]

TABLE_PATH = "open-parking-spaces.spaces.lot_spaces"


def scrape(event, context, dry_run=False):
    bq_client = bigquery.Client()
    timestamp = datetime.datetime.utcnow()
    errors = []
    for scraper_class in SCRAPER_CLASSES:
        logger.info(f"Processing scraper class {scraper_class}")
        scraper = scraper_class()
        try:
            scraper.scrape(bq_client, TABLE_PATH, timestamp, dry_run=dry_run)
        except Exception as error:
            logger.exception(error)
            errors.append(error)
    if len(errors) > 0:
        raise ValueError(errors)


if __name__ == "__main__":
    scrape({}, {}, dry_run=True)
