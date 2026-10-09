# Automated Web Scraping & Data Extraction Pipeline

A Python ETL web scraper using Requests and BeautifulSoup. It targets **Books to Scrape**, a public practice website for scraping exercises: https://books.toscrape.com/

## What it does
- Selects a public scraping target
- Sends requests with a custom User-Agent
- Applies 1-second rate limiting
- Retries transient failures with exponential backoff
- Parses HTML with BeautifulSoup
- Cleans and deduplicates records
- Saves structured CSV and JSON
- Generates an automated statistics report

## Extracted fields
`title`, `price_gbp`, `availability`, `rating`, `category`, `product_url`

## Run
```bash
pip install -r requirements.txt
python main.py --pages 3
```

Outputs:
- `data/books.csv`
- `data/books.json`
- `reports/summary_report.txt`

## ETL flow
Website → Request → Rate Limit/Retry → HTML → BeautifulSoup → Transform → CSV/JSON → Summary Report

## Responsible scraping
This project uses Books to Scrape because it is intended for scraping practice. For other sites, check their terms, robots.txt, access policies, and applicable laws before collecting data.
