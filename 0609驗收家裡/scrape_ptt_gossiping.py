import csv
from pathlib import Path
from urllib.parse import urljoin

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


TARGET_URL = "https://www.ptt.cc/bbs/Gossiping/index.html"
BASE_URL = "https://www.ptt.cc"
OUTPUT_CSV = Path(__file__).with_name("ptt_gossiping.csv")


def pass_age_check(page):
    """Click the age confirmation button if PTT shows the over-18 page."""
    if "over18" not in page.url:
        return

    page.locator("button[name='yes']").click()
    page.wait_for_load_state("networkidle")


def scrape_articles(page):
    page.wait_for_selector(".r-ent", timeout=10000)

    articles = []
    rows = page.locator(".r-ent")

    for index in range(rows.count()):
        row = rows.nth(index)

        nrec = row.locator(".nrec").inner_text().strip()
        title_locator = row.locator(".title a")
        title_text = row.locator(".title").inner_text().strip()
        author = row.locator(".author").inner_text().strip()
        date = row.locator(".date").inner_text().strip()

        if title_locator.count() > 0:
            title = title_locator.inner_text().strip()
            href = title_locator.get_attribute("href")
            url = urljoin(BASE_URL, href)
        else:
            title = title_text
            url = ""

        articles.append(
            {
                "nrec": nrec,
                "title": title,
                "author": author,
                "date": date,
                "url": url,
            }
        )

    return articles


def save_csv(articles, output_path):
    with output_path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["nrec", "title", "author", "date", "url"],
        )
        writer.writeheader()
        writer.writerows(articles)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            page.goto(TARGET_URL, wait_until="domcontentloaded")
            pass_age_check(page)
            articles = scrape_articles(page)
            save_csv(articles, OUTPUT_CSV)
            print(f"Saved {len(articles)} rows to {OUTPUT_CSV}")
        except PlaywrightTimeoutError as error:
            print(f"Timed out while waiting for page content: {error}")
        finally:
            browser.close()


if __name__ == "__main__":
    main()
