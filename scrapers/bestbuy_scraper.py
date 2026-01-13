from typing import Dict, List, Optional
from .base_scraper import BaseScraper
import logging
from bs4 import BeautifulSoup
import urllib.parse

logger = logging.getLogger(__name__)

class BestBuyScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.bestbuy.ca"
        
    async def scrape(self, product_name: str) -> Optional[List[Dict]]:
        try:
            cached_result = self.get_cached_result(product_name)
            if cached_result:
                return cached_result

            encoded_query = urllib.parse.quote(product_name)
            search_url = f"{self.base_url}/en-ca/search?search={encoded_query}"
            
            html_content = await self.make_request(search_url)
            
            if html_content:
                soup = BeautifulSoup(html_content, 'lxml')
                product_elem = soup.find('div', {'class': 'x-productListItem'})
                
                if product_elem:
                    price_elem = product_elem.find('span', {'class': 'price_FHDfG large_3gQAp'})
                    title_elem = product_elem.find('div', {'class': 'productItemName_3IZ3c'})
                    product_url = product_elem.find('a', {'class': 'link_3hcyN'})
                    
                    if price_elem and title_elem:
                        result = [{
                            'brand': self.extract_brand(product_name),
                            'website': 'Best Buy',
                            'title': title_elem.text.strip(),
                            'price': self.clean_price(price_elem.text),
                            'price_valid_till': '',
                            'url': f"{self.base_url}{product_url.get('href')}" if product_url else search_url
                        }]
                        
                        self.cache_result(product_name, result)
                        return result
            
            logger.info(f"No results found for {product_name} at Best Buy. URL: {search_url}")
            return None
            
        except Exception as e:
            logger.error(f"Error in Best Buy scraper: {str(e)}")
            return None

    def _extract_model_number(self, product_name: str) -> str:
        """Extract model number from product name using BestBuy specific logic"""
        try:
            # First try to find the model after a hyphen
            if '-' in product_name:
                return product_name.split('-')[-1].strip()
            
            # Look for common model number patterns
            import re
            patterns = [
                r'[A-Z0-9]{2,}[A-Z][0-9]{2,}[A-Z0-9]*',  # Common TV model format
                r'[A-Z]{2,}[0-9]{2,}[A-Z]*[0-9]*'        # Alternative format
            ]
            
            for pattern in patterns:
                match = re.search(pattern, product_name)
                if match:
                    return match.group(0)
            
            return product_name
        except Exception as e:
            logger.warning(f"Error extracting model number: {str(e)}")
            return product_name 