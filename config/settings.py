import os
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
LOGS_DIR = BASE_DIR / 'logs'
RESULTS_DIR = DATA_DIR / 'results'

# Create necessary directories
for directory in [DATA_DIR, LOGS_DIR, RESULTS_DIR]:
    directory.mkdir(exist_ok=True)

# Scraping settings
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 5
CONCURRENT_REQUESTS = 3

# Cache settings
CACHE_ENABLED = True
CACHE_DURATION = 3600  # 1 hour
CACHE_DIR = DATA_DIR / 'cache'

# Rate limiting settings
RATE_LIMIT = {
    'bestbuy': {'requests': 10, 'period': 60},  # 10 requests per minute
    'amazon': {'requests': 5, 'period': 60},    # 5 requests per minute
    'costco': {'requests': 8, 'period': 60},    # 8 requests per minute
    'default': {'requests': 5, 'period': 60}    # Default rate limit
}

# Proxy settings
PROXY_ENABLED = False
PROXY_LIST = []  # Add your proxy list here
PROXY_AUTH = None  # Add proxy authentication if needed

# API Keys (store these in environment variables in production)
API_KEYS = {
    'amazon': os.getenv('AMAZON_API_KEY'),
    'bestbuy': os.getenv('BESTBUY_API_KEY'),
} 