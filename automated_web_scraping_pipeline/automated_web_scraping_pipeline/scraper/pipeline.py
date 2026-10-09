import csv
import json
import logging
from pathlib import Path
from .config import BASE_URL
from .http_client import HttpClient
from .parser import parse_books
from .report import generate_summary, save_report

logger = logging.getLogger(__name__)

class ScrapingPipeline:
    """ETL: extract HTML, transform records, load CSV/JSON, report statistics."""
    def __init__(self, client=None):
        self.client = client or HttpClient()

    def extract(self, pages: int):
        records, succeeded = [], 0
        for page in range(1, pages + 1):
            url = BASE_URL.format(page=page)
            try:
                html = self.client.get(url)
                page_records = parse_books(html, url)
                records.extend(page_records)
                succeeded += 1
                logger.info("Parsed %d records from page %d", len(page_records), page)
            except Exception as exc:
                logger.error("Skipping page %d: %s", page, exc)
        return records, succeeded

    @staticmethod
    def transform(records):
        cleaned, seen = [], set()
        for r in records:
            if r["product_url"] in seen:
                continue
            cleaned.append({
                "title": " ".join(r["title"].split()),
                "price_gbp": float(r["price_gbp"]),
                "availability": " ".join(r["availability"].split()),
                "rating": r["rating"],
                "category": " ".join(r["category"].split()),
                "product_url": r["product_url"],
            })
            seen.add(r["product_url"])
        return cleaned

    @staticmethod
    def load_csv(records, path):
        path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
        fields = ["title","price_gbp","availability","rating","category","product_url"]
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields); writer.writeheader(); writer.writerows(records)

    @staticmethod
    def load_json(records, path):
        path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)

    def run(self, pages, output_dir="data", report_dir="reports"):
        raw, succeeded = self.extract(pages)
        records = self.transform(raw)
        csv_path = Path(output_dir) / "books.csv"
        json_path = Path(output_dir) / "books.json"
        report_path = Path(report_dir) / "summary_report.txt"
        self.load_csv(records, csv_path)
        self.load_json(records, json_path)
        save_report(generate_summary(records, pages, succeeded), report_path)
        return {"records": records, "pages_succeeded": succeeded, "csv": str(csv_path), "json": str(json_path), "report": str(report_path)}
