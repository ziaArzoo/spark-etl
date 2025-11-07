import requests, time, logging
from typing import Dict, Any

class APIClient:

    def __init__(self, base_url: str, params: Dict[str, Any],
                 max_retries: int = 3, backoff: int = 2):
        self.base_url = base_url
        self.params = params
        self.max_retries = max_retries
        self.backoff = backoff
        self.logger = logging.getLogger(__name__)

    def fetch(self) -> Dict[str, Any]:
        attempt = 0
        while attempt < self.max_retries:
            try:
                res = requests.get(self.base_url, params=self.params, timeout=30)
                res.raise_for_status()
                return res.json()
            except requests.RequestException as e:
                attempt += 1
                self.logger.warning(f"Attempt {attempt} failed: {e}")
                if attempt < self.max_retries:
                    time.sleep(self.backoff ** attempt)
                else:
                    raise
