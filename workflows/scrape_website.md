# Workflow: Scrape a Website

## Objective
Extract readable text content from one or more web pages and save it for downstream processing.

## Required Inputs
| Input | Description |
|-------|-------------|
| `url` | The full URL of the page to scrape |
| `output_path` | (optional) Where to save the result, e.g. `.tmp/scraped.txt` |

## Tool to Use
`tools/scrape_single_site.py`

## Steps
1. Confirm the URL is accessible (not behind a login wall or bot protection).
2. Run the tool:
   ```bash
   python tools/scrape_single_site.py --url <URL> --output .tmp/scraped.txt
   ```
3. Verify `.tmp/scraped.txt` contains meaningful text (not just nav/footer noise).
4. Pass the file path to the next workflow step that needs the content.

## Expected Output
A plain-text file with the page's readable content, stripped of scripts and styling.

## Edge Cases & Known Constraints
- **Bot protection (403/429):** Some sites block scrapers. Try adding a delay or a more realistic User-Agent. Document any site-specific workarounds here.
- **JavaScript-rendered pages:** The current tool uses `requests` + `BeautifulSoup` and cannot execute JS. For SPA pages, a Playwright-based tool will be needed.
- **Rate limits:** If scraping multiple pages, add a 1–2 s sleep between requests to avoid bans.

## Notes
_Update this section whenever you discover new constraints or better approaches._
