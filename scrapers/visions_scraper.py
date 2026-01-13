from typing import Dict, List, Optional
from .base_scraper import BaseScraper
import logging
from bs4 import BeautifulSoup
import urllib.parse

logger = logging.getLogger(__name__)

class VisionsScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.visions.ca"
        
    async def scrape(self, product_name: str) -> Optional[List[Dict]]:
        try:
            # Check cache first
            cached_result = self.get_cached_result(product_name)
            if cached_result:
                return cached_result

            # Encode the full product name
            encoded_query = urllib.parse.quote(product_name)
            
            # Use the catalog search URL
            search_url = f"{self.base_url}/catalogsearch/result?q={encoded_query}"
            
            # Make async request
            html_content = await self.make_request(search_url)
            
            if html_content:
                soup = BeautifulSoup(html_content, 'lxml')
                
                # Find the first product in search results
                product_elem = soup.find('li', {'class': 'item product product-item'})
                
                if product_elem:
                    # Extract product details
                    price_elem = product_elem.find('span', {'class': 'price'})
                    title_elem = product_elem.find('a', {'class': 'product-item-link'})
                    product_url = title_elem.get('href') if title_elem else None
                    
                    if price_elem and title_elem:
                        result = [{
                            'brand': self.extract_brand(product_name),
                            'website': 'Visions',
                            'title': title_elem.text.strip(),
                            'price': self.clean_price(price_elem.text),
                            'price_valid_till': '',
                            'url': product_url or search_url
                        }]
                        
                        # Cache the result
                        self.cache_result(product_name, result)
                        return result
            
            logger.info(f"No results found for {product_name} at Visions. URL: {search_url}")
            return None
            
        except Exception as e:
            logger.error(f"Error in Visions scraper: {str(e)}")
            return None

    def clean_price(self, price_text: str) -> str:
        """Clean price text by removing currency symbols and whitespace"""
        try:
            cleaned = ''.join(c for c in price_text if c.isdigit() or c == '.')
            return cleaned
        except Exception as e:
            logger.error(f"Error cleaning price text: {str(e)}")
            return price_text