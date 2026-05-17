import time
import requests
import gspread
import argparse
from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials

# ---------------------------------------------------------------------------
# Known location → geoId mappings (add more as needed)
# Find geoId by searching LinkedIn manually and inspecting the URL
# ---------------------------------------------------------------------------
GEO_IDS = {
    "united states":    "103644278",
    "united kingdom":   "101165590",
    "canada":           "101174742",
    "australia":        "101452733",
    "germany":          "101282230",
    "france":           "105015875",
    "india":            "102713980",
    "singapore":        "102454443",
    "remote":           "92000000",
    "bangladesh":       "",
}


def build_url(location: str, keyword: str = "", geo_id: str = "") -> str:
    params = {
        "keywords": keyword,
        "location": location,
        "trk": "public_jobs_jobs-search-bar_search-submit",
    }
    if geo_id:
        params["geoId"] = geo_id
    return "https://www.linkedin.com/jobs/search?" + urlencode(params)


def make_headless_driver() -> webdriver.Chrome:
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=opts)


def scroll_and_get_html(url: str) -> str:
    driver = make_headless_driver()
    driver.get(url)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    html = driver.page_source
    driver.quit()
    return html


def parse_job_listings(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.find_all("div", class_="base-card")
    jobs = []
    for card in cards:
        time_new = card.find("time", class_="job-search-card__listdate--new")
        time_old = card.find("time", class_="job-search-card__listdate")
        time_el = time_old or time_new
        if not time_el:
            continue
        posted_date = time_el.get("datetime", "")
        jobs.append({
            "JobID":               card.get("data-row", ""),
            "ID":                  card.get("data-tracking-id", ""),
            "name":                (card.find("span", class_="sr-only") or {}).get_text(strip=True),
            "hiring_company":      (card.find("h4", class_="base-search-card__subtitle") or {}).get_text(strip=True),
            "location":            (card.find("span", class_="job-search-card__location") or {}).get_text(strip=True),
            "posted_time_friendly": time_el.get_text(strip=True),
            "posted_time":         posted_date,
            "themonth":            posted_date[5:7],
            "theyear":             posted_date[:4],
            "theurl":              (card.find("a", class_="base-card__full-link") or {}).get("href", ""),
            "source":              "LinkedIn",
        })
    return jobs


def fetch_job_detail(job_url: str, max_retries: int = 15) -> tuple[str, list[tuple]]:
    """Returns (description, industry_criteria_list)."""
    description = ""
    criteria = []

    for attempt in range(max_retries):
        try:
            resp = requests.get(job_url, timeout=10)
            if resp.status_code != 200:
                time.sleep(1)
                continue
            soup = BeautifulSoup(resp.content, "html.parser")
            desc_el = soup.find("div", class_="show-more-less-html__markup")
            if desc_el:
                description = desc_el.get_text(strip=True)
                criteria = _extract_criteria(soup)
                return description, criteria
        except requests.RequestException:
            time.sleep(1)

    # Fallback to Selenium if requests keeps failing
    try:
        driver = make_headless_driver()
        driver.get(job_url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()
        desc_el = soup.find("div", class_="show-more-less-html__markup")
        if desc_el:
            description = desc_el.get_text(strip=True)
        criteria = _extract_criteria(soup)
    except Exception as e:
        print(f"  Selenium fallback failed for {job_url}: {e}")

    return description, criteria


def _extract_criteria(soup: BeautifulSoup) -> list[tuple]:
    items = soup.find_all("li", class_="description__job-criteria-item")
    result = []
    for item in items:
        heading = item.find("h3", class_="description__job-criteria-subheader")
        value = item.find("span", class_="description__job-criteria-text--criteria")
        if heading and value:
            result.append((heading.get_text(strip=True), value.get_text(strip=True)))
    return result


def scrape_location(location: str, keyword: str = "", geo_id: str = "") -> list[dict]:
    geo_id = geo_id or GEO_IDS.get(location.lower(), "")
    url = build_url(location, keyword, geo_id)
    print(f"\nScraping: {url}")

    html = scroll_and_get_html(url)
    jobs = parse_job_listings(html)
    print(f"Found {len(jobs)} job listings for '{location}'")

    for i, job in enumerate(jobs):
        print(f"  [{i+1}/{len(jobs)}] Fetching details: {job['name']} @ {job['hiring_company']}")
        desc, criteria = fetch_job_detail(job["theurl"])
        job["snippet"] = desc
        for key, val in criteria:
            job[key] = val

    return jobs


def push_to_sheets(all_jobs: list[dict], sheet_name: str = "Job Feed", tab_name: str = "Jobs"):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("JSON.json", scope)
    client = gspread.authorize(creds)
    worksheet = client.open(sheet_name).worksheet(tab_name)

    # Collect all unique keys (columns) in order
    all_keys: list[str] = []
    seen = set()
    for job in all_jobs:
        for k in job:
            if k not in seen:
                all_keys.append(k)
                seen.add(k)

    rows = [[job.get(k, "") for k in all_keys] for job in all_jobs]

    worksheet.clear()
    worksheet.append_row(all_keys)
    worksheet.append_rows(rows)
    print(f"\nUploaded {len(all_jobs)} jobs to Google Sheets.")
    print("Spreadsheet:", worksheet.url)


def main():
    parser = argparse.ArgumentParser(description="LinkedIn Public Jobs Scraper")
    parser.add_argument(
        "--locations", nargs="+",
        default=["Cayman Islands"],
        help='One or more locations, e.g. --locations "United States" "Canada" "Remote"',
    )
    parser.add_argument(
        "--keyword", default="",
        help='Job keyword filter, e.g. --keyword "Software Engineer"',
    )
    parser.add_argument(
        "--geo-ids", nargs="+", default=[],
        help="Optional geoIds matching each location in order",
    )
    parser.add_argument(
        "--no-sheets", action="store_true",
        help="Skip uploading to Google Sheets (print count only)",
    )
    args = parser.parse_args()

    geo_ids = args.geo_ids + [""] * len(args.locations)  # pad with empty strings

    all_jobs: list[dict] = []
    for i, location in enumerate(args.locations):
        jobs = scrape_location(location, keyword=args.keyword, geo_id=geo_ids[i])
        all_jobs.extend(jobs)

    print(f"\nTotal jobs scraped across all locations: {len(all_jobs)}")

    if not args.no_sheets and all_jobs:
        push_to_sheets(all_jobs)


if __name__ == "__main__":
    main()
