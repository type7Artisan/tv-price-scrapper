"""
Configuration package for TV price scraper.
"""

from .settings import (
    BASE_DIR,
    DATA_DIR,
    LOGS_DIR,
    RESULTS_DIR,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY,
    CONCURRENT_REQUESTS,
    CACHE_ENABLED,
    CACHE_DURATION,
    CACHE_DIR,
    RATE_LIMIT,
    PROXY_ENABLED,
    PROXY_LIST,
    PROXY_AUTH,
    API_KEYS,
)

__all__ = [
    'BASE_DIR',
    'DATA_DIR',
    'LOGS_DIR',
    'RESULTS_DIR',
    'REQUEST_TIMEOUT',
    'MAX_RETRIES',
    'RETRY_DELAY',
    'CONCURRENT_REQUESTS',
    'CACHE_ENABLED',
    'CACHE_DURATION',
    'CACHE_DIR',
    'RATE_LIMIT',
    'PROXY_ENABLED',
    'PROXY_LIST',
    'PROXY_AUTH',
    'API_KEYS',
]
