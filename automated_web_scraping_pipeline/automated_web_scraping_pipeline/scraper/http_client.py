import logging
import time
import requests
from .config import BACKOFF_FACTOR, HEADERS, MAX_RETRIES, REQUEST_DELAY_SECONDS, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

class HttpClient:
    """HTTP client with custom headers, rate limiting, and retry logic."""
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self._last_request_time = 0.0

    def _rate_limit(self):
        remaining = REQUEST_DELAY_SECONDS - (time.monotonic() - self._last_request_time)
        if remaining > 0:
            time.sleep(remaining)

    def get(self, url: str) -> str:
        last_error = None
        for attempt in range(1, MAX_RETRIES + 1):
            self._rate_limit()
            try:
                logger.info("GET %s (attempt %d/%d)", url, attempt, MAX_RETRIES)
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                self._last_request_time = time.monotonic()
                if response.status_code == 429 or 500 <= response.status_code < 600:
                    raise requests.HTTPError(f"Retryable HTTP status: {response.status_code}")
                response.raise_for_status()
                return response.text
            except requests.RequestException as exc:
                last_error = exc
                logger.warning("Request failed: %s", exc)
                if attempt < MAX_RETRIES:
                    delay = BACKOFF_FACTOR * (2 ** (attempt - 1))
                    time.sleep(delay)
        raise RuntimeError(f"Failed to fetch {url}: {last_error}")
