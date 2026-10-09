BASE_URL = "https://books.toscrape.com/catalogue/page-{page}.html"
DEFAULT_PAGES = 3
REQUEST_TIMEOUT = 15
REQUEST_DELAY_SECONDS = 1.0
MAX_RETRIES = 3
BACKOFF_FACTOR = 1.5
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; EducationalScraper/1.0)",
    "Accept": "text/html,application/xhtml+xml",
}
