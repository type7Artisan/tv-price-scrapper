from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import aiohttp
import asyncio
import re
import logging
import os
import json
from bs4 import BeautifulSoup
from utils.cache import Cache
from utils.rate_limiter import RateLimiter
from config.settings import REQUEST_TIMEOUT, MAX_RETRIES, RETRY_DELAY

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.cache = Cache()
        self.rate_limiter = RateLimiter()

    @abstractmethod
    async def scrape(self, product_name: str) -> Optional[List[Dict]]:
        pass

    async def make_request(self, url: str, params: Optional[Dict] = None) -> str:
        """Make an async HTTP request"""
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=self.headers) as response:
                if response.status == 200:
                    return await response.text()
                response.raise_for_status()

    def extract_brand(self, product_name: str) -> str:
        brands = ['Samsung', 'LG', 'Hisense', 'SONY']
        for brand in brands:
            if brand.lower() in product_name.lower():
                return brand
        return 'Unknown'

    def clean_price(self, price: str) -> str:
        return re.sub(r'[^\d.]', '', price)

    def _get_safe_filename(self, filename: str) -> str:
        """Convert string to a safe filename by removing or replacing invalid characters"""
        safe_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        safe_filename = safe_filename.replace('"', '').replace("'", "")
        safe_filename = safe_filename[:200]
        return safe_filename

    def get_cache_path(self, product_name: str) -> str:
        """Get the cache file path for a product"""
        safe_name = self._get_safe_filename(product_name)
        return os.path.join('data', 'cache', f"{self.__class__.__name__}_{safe_name}.json")

    def get_cached_result(self, product_name: str) -> Optional[List[Dict]]:
        """Get cached results for a product if they exist"""
        try:
            cache_path = self.get_cache_path(product_name)
            if os.path.exists(cache_path):
                with open(cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Cache read error for {product_name}: {str(e)}")
        return None

    def cache_result(self, product_name: str, result: List[Dict]) -> None:
        """Cache results for a product"""
        try:
            cache_path = self.get_cache_path(product_name)
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.warning(f"Cache write error for {product_name}: {str(e)}") 