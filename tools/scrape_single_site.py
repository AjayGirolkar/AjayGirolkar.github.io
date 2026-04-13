"""
Tool: scrape_single_site.py
Purpose: Fetch the raw HTML (or cleaned text) from a single URL.

Usage:
    python tools/scrape_single_site.py --url https://example.com [--output .tmp/page.html]
"""

import argparse
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def scrape(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; WAT-scraper/1.0)"}
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove script / style noise
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    return soup.get_text(separator="\n", strip=True)


def main():
    parser = argparse.ArgumentParser(description="Scrape a single web page.")
    parser.add_argument("--url", required=True, help="URL to scrape")
    parser.add_argument("--output", default=None, help="Optional file path to save the result")
    args = parser.parse_args()

    try:
        text = scrape(args.url)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"Saved to {out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
