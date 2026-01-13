"""
Scrapers package for TV price scraping from various retailers.
"""

from .visions_scraper import VisionsScraper
from .amazon_scraper import AmazonScraper
from .bestbuy_scraper import BestBuyScraper
from .costco_scraper import CostcoScraper
from .canadiantire_scraper import CanadianTireScraper
from .londondrugs_scraper import LondonDrugsScraper
from .dufresne_scraper import DufresneScraper
from .tanguay_scraper import TanguayScraper
from .teppermans_scraper import TeppermansScraper
from .lg_scraper import LGScraper
from .samsung_scraper import SamsungScraper
from .staples_scraper import StaplesScraper

__all__ = [
    'VisionsScraper',
    'AmazonScraper',
    'BestBuyScraper',
    'CostcoScraper',
    'CanadianTireScraper',
    'LondonDrugsScraper',
    'DufresneScraper',
    'TanguayScraper',
    'TeppermansScraper',
    'LGScraper',
    'SamsungScraper',
    'StaplesScraper',
]
