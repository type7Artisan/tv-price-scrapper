import pytest
from scrapers.staples_scraper import StaplesScraper
from utils.validators import ProductValidationError

@pytest.fixture
def scraper():
    return StaplesScraper()

def test_scraper_initialization(scraper):
    assert scraper.base_url == "https://www.staples.ca"
    assert scraper.search_url == "https://www.staples.ca/graphql"
    assert all(key in scraper.headers for key in [
        'Accept', 'Content-Type', 'Store', 'X-Locale'
    ])

@pytest.mark.asyncio
async def test_valid_product_scraping(scraper):
    product_name = 'Samsung 65" 4K Tizen Smart QLED TV - QN65Q60DAFXZC'
    result = await scraper.scrape(product_name)
    
    if result:
        product = result[0]
        assert all(key in product for key in [
            'brand', 'website', 'title', 'price', 
            'regular_price', 'url', 'sku', 'availability'
        ])
        assert product['brand'] == 'Samsung'
        assert product['website'] == 'Staples'
        assert isinstance(float(product['price']), float)
        assert product['url'].startswith('https://www.staples.ca/')

@pytest.mark.asyncio
async def test_invalid_product_scraping(scraper):
    product_name = 'NonexistentProduct12345'
    result = await scraper.scrape(product_name)
    assert result is None or len(result) == 0

def test_model_number_extraction(scraper):
    test_cases = [
        ('Samsung TV - QN65Q60DAFXZC', 'QN65Q60DAFXZC'),
        ('LG OLED65C1PUB 65" TV', 'OLED65C1PUB'),
        ('Sony XR65A80K', 'XR65A80K'),
        ('TCL 65R635 65" TV', '65R635'),
    ]
    
    for input_name, expected in test_cases:
        assert scraper._extract_model_number(input_name) == expected

@pytest.mark.asyncio
async def test_price_validation(scraper):
    product_name = 'Samsung 65" 4K TV - QN65Q60DAFXZC'
    result = await scraper.scrape(product_name)
    
    if result:
        product = result[0]
        price = float(product['price'])
        assert 100 <= price <= 10000  # Reasonable TV price range

@pytest.mark.asyncio
async def test_promotional_pricing(scraper):
    """Test that promotional and sale prices are handled correctly"""
    product_name = 'Samsung 65" 4K TV - QN65Q60DAFXZC'
    result = await scraper.scrape(product_name)
    
    if result:
        product = result[0]
        # Check that at least one price type exists
        assert any([
            product.get('regular_price'),
            product.get('sale_price'),
            product.get('promotional_price')
        ])
        # If there's a promotional price, it should be less than regular price
        if product.get('promotional_price'):
            assert float(product['promotional_price']) <= float(product['regular_price']) 