import argparse
import logging
from scraper.config import DEFAULT_PAGES
from scraper.pipeline import ScrapingPipeline


def main():
    parser = argparse.ArgumentParser(description="Automated web scraping ETL pipeline")
    parser.add_argument("--pages", type=int, default=DEFAULT_PAGES)
    args = parser.parse_args()
    if args.pages < 1:
        raise SystemExit("--pages must be at least 1")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    result = ScrapingPipeline().run(args.pages)
    print("\n" + "=" * 55)
    print("AUTOMATED WEB SCRAPING PIPELINE")
    print("=" * 55)
    print(f"Pages successfully scraped : {result['pages_succeeded']}")
    print(f"Records extracted          : {len(result['records'])}")
    print(f"CSV output                 : {result['csv']}")
    print(f"JSON output                : {result['json']}")
    print(f"Summary report             : {result['report']}")


if __name__ == "__main__":
    main()
