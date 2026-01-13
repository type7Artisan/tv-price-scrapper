import pytest
from scrapers.canadiantire_scraper import CanadianTireScraper
from utils.validators import ProductValidationError

@pytest.fixture
def scraper():
    return CanadianTireScraper()

def test_scraper_initialization(scraper):
    assert scraper.base_url == "https://www.canadiantire.ca"

@pytest.mark.asyncio
async def test_valid_product_scraping(scraper):
    product_name = 'Samsung 65" 4K Tizen Smart QLED TV - QN65Q60DAFXZC'
    result = await scraper.scrape(product_name)
    
    if result:
        product = result[0]
        assert 'brand' in product
        assert 'website' in product
        assert 'title' in product
        assert 'price' in product
        assert product['brand'] == 'Samsung'
        assert product['website'] == 'Canadian Tire'

@pytest.mark.asyncio
async def test_invalid_product_scraping(scraper):
    product_name = 'NonexistentProduct12345'
    result = await scraper.scrape(product_name)
    assert result is None or len(result) == 0 