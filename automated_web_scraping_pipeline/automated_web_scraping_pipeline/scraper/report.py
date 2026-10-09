from collections import Counter
from pathlib import Path
from statistics import mean


def generate_summary(records: list[dict], pages_requested: int, pages_succeeded: int) -> str:
    if not records:
        return "No records were collected."
    prices = [r["price_gbp"] for r in records]
    ratings = Counter(r["rating"] for r in records)
    categories = Counter(r["category"] for r in records)
    lines = [
        "AUTOMATED WEB SCRAPING SUMMARY REPORT", "=" * 42,
        f"Pages requested : {pages_requested}", f"Pages succeeded : {pages_succeeded}",
        f"Records scraped : {len(records)}", "", "PRICE STATISTICS", "-" * 20,
        f"Minimum price   : £{min(prices):.2f}", f"Maximum price   : £{max(prices):.2f}",
        f"Average price   : £{mean(prices):.2f}", "", "RATING DISTRIBUTION", "-" * 20,
    ]
    lines += [f"{k:<10}: {v}" for k, v in sorted(ratings.items())]
    lines += ["", "CATEGORY DISTRIBUTION", "-" * 20]
    lines += [f"{k:<25}: {v}" for k, v in categories.most_common()]
    lines += ["", "Generated automatically by the ETL scraping pipeline."]
    return "\n".join(lines)


def save_report(report: str, path: str | Path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report, encoding="utf-8")
