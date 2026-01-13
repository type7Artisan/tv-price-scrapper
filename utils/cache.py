import json
import time
from pathlib import Path
from typing import Any, Optional
from config.settings import CACHE_DIR, CACHE_DURATION

class Cache:
    def __init__(self):
        self.cache_dir = Path(CACHE_DIR)
        self.cache_dir.mkdir(exist_ok=True)

    def _get_cache_path(self, key: str) -> Path:
        return self.cache_dir / f"{key}.json"

    def get(self, key: str) -> Optional[Any]:
        cache_path = self._get_cache_path(key)
        if not cache_path.exists():
            return None

        try:
            with cache_path.open('r') as f:
                data = json.load(f)
                if time.time() - data['timestamp'] > CACHE_DURATION:
                    cache_path.unlink()
                    return None
                return data['value']
        except Exception:
            return None

    def set(self, key: str, value: Any) -> None:
        cache_path = self._get_cache_path(key)
        data = {
            'timestamp': time.time(),
            'value': value
        }
        with cache_path.open('w') as f:
            json.dump(data, f)

    def clear(self) -> None:
        for cache_file in self.cache_dir.glob('*.json'):
            cache_file.unlink() 