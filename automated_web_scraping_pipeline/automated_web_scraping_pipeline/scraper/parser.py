from urllib.parse import urljoin
from bs4 import BeautifulSoup


def parse_books(html: str, page_url: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    records = []
    for article in soup.select("article.product_pod"):
        title_link = article.select_one("h3 a")
        price_tag = article.select_one(".price_color")
        availability_tag = article.select_one(".availability")
        rating_tag = article.select_one("p.star-rating")
        if not title_link or not price_tag:
            continue
        rating_classes = rating_tag.get("class", []) if rating_tag else []
        rating = next((x for x in rating_classes if x in {"One","Two","Three","Four","Five"}), "Unknown")
        relative_url = title_link.get("href", "")
        records.append({
            "title": (title_link.get("title") or title_link.get_text(strip=True)).strip(),
            "price_gbp": clean_price(price_tag.get_text(" ", strip=True)),
            "availability": availability_tag.get_text(" ", strip=True) if availability_tag else "Unknown",
            "rating": rating,
            "category": extract_category(soup),
            "product_url": urljoin(page_url, relative_url),
        })
    return records


def clean_price(price_text: str) -> float:
    return round(float(price_text.replace("£", "").replace(",", "").strip()), 2)


def extract_category(soup: BeautifulSoup) -> str:
    breadcrumb = soup.select("ul.breadcrumb li")
    return breadcrumb[2].get_text(" ", strip=True) if len(breadcrumb) >= 3 else "Unknown"
