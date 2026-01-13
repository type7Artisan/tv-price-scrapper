from typing import Dict, List, Optional
from .base_scraper import BaseScraper
import logging
from bs4 import BeautifulSoup
import urllib.parse

logger = logging.getLogger(__name__)

class TanguayScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.tanguay.ca"

    async def scrape(self, product_name: str) -> Optional[List[Dict]]:
        try:
            cached_result = self.get_cached_result(product_name)
            if cached_result:
                return cached_result

            encoded_query = urllib.parse.quote(product_name)
            search_url = f"{self.base_url}/en/search?q={encoded_query}"
            
            html_content = await self.make_request(search_url)
            
            if html_content:
                soup = BeautifulSoup(html_content, 'lxml')
                product_elem = soup.find('div', {'class': 'product-item'})
                
                if product_elem:
                    price_elem = product_elem.find('span', {'class': 'price'})
                    title_elem = product_elem.find('h3', {'class': 'product-name'})
                    product_url = product_elem.find('a', {'class': 'product-link'})
                    
                    if price_elem and title_elem:
                        result = [{
                            'brand': self.extract_brand(product_name),
                            'website': 'Tanguay',
                            'title': title_elem.text.strip(),
                            'price': self.clean_price(price_elem.text),
                            'price_valid_till': '',
                            'url': f"{self.base_url}{product_url.get('href')}" if product_url else search_url
                        }]
                        
                        self.cache_result(product_name, result)
                        return result
            
            logger.info(f"No results found for {product_name} at Tanguay. URL: {search_url}")
            return None
            
        except Exception as e:
            logger.error(f"Error in Tanguay scraper: {str(e)}")
            return None 