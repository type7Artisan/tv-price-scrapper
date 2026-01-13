from typing import Dict, List, Optional
from .base_scraper import BaseScraper
import logging
from bs4 import BeautifulSoup
import urllib.parse

logger = logging.getLogger(__name__)

class CanadianTireScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.canadiantire.ca"

    async def scrape(self, product_name: str) -> Optional[List[Dict]]:
        try:
            cached_result = self.get_cached_result(product_name)
            if cached_result:
                return cached_result

            encoded_query = urllib.parse.quote(product_name)
            search_url = f"{self.base_url}/en/search-results?q={encoded_query}"
            
            html_content = await self.make_request(search_url)
            
            if html_content:
                soup = BeautifulSoup(html_content, 'lxml')
                product_elem = soup.find('div', {'class': 'product-tile'})
                
                if product_elem:
                    price_elem = product_elem.find('span', {'class': 'price__amount'})
                    title_elem = product_elem.find('h3', {'class': 'product-tile__title'})
                    product_url = product_elem.find('a', {'class': 'product-tile__link'})
                    
                    if price_elem and title_elem:
                        result = [{
                            'brand': self.extract_brand(product_name),
                            'website': 'Canadian Tire',
                            'title': title_elem.text.strip(),
                            'price': self.clean_price(price_elem.text),
                            'price_valid_till': '',
                            'url': f"{self.base_url}{product_url.get('href')}" if product_url else search_url
                        }]
                        
                        self.cache_result(product_name, result)
                        return result
            
            logger.info(f"No results found for {product_name} at Canadian Tire. URL: {search_url}")
            return None
            
        except Exception as e:
            logger.error(f"Error in Canadian Tire scraper: {str(e)}")
            return None 