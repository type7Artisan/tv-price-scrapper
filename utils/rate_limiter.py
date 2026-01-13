import time
from collections import defaultdict
from threading import Lock
from typing import Dict
from config.settings import RATE_LIMIT

class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
        self.locks = defaultdict(Lock)

    def wait(self, website: str) -> None:
        with self.locks[website]:
            rate_config = RATE_LIMIT.get(website, RATE_LIMIT['default'])
            current_time = time.time()
            
            # Remove old requests
            self.requests[website] = [
                req_time for req_time in self.requests[website]
                if current_time - req_time < rate_config['period']
            ]
            
            # If we've hit the limit, wait
            if len(self.requests[website]) >= rate_config['requests']:
                sleep_time = (
                    self.requests[website][0] +
                    rate_config['period'] -
                    current_time
                )
                if sleep_time > 0:
                    time.sleep(sleep_time)
            
            # Add current request
            self.requests[website].append(current_time) 