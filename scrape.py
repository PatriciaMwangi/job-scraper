import asyncio
import csv
import os
import urllib.parse
from datetime import datetime
from playwright.async_api import async_playwright

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(SCRIPT_DIR, "jobs.csv")
FIELDNAMES = ["job_url", "title", "company", "date_posted", "description", "scraped_at"]


def load_existing_urls(filepath):
    """
    Read the CSV (if it exists) and return a set of job_urls we already have.
    A 'set' is used because checking 'is this URL already in here?' is
    very fast with a set, compared to a list.
    """
    existing_urls = set()
    if os.path.exists(filepath):
        with open(filepath, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_urls.add(row["job_url"])
    return existing_urls


def append_jobs_to_csv(filepath, jobs, existing_urls):
    """
    Append only the jobs whose URL we haven't already saved.
    Returns how many new rows were actually written.
    """
    file_exists = os.path.exists(filepath)
    new_count = 0

    # 'a' mode = append (add to the end, don't overwrite the file)
    with open(filepath, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)

        # Only write the header row once, when the file is brand new
        if not file_exists:
            writer.writeheader()

        for job in jobs:
            if job["job_url"] not in existing_urls:
                writer.writerow(job)
                existing_urls.add(job["job_url"])  # remember it for this run too
                new_count += 1

    return new_count


async def scrape_myjobmag(query="software engineering", location="Nairobi"):
    q = urllib.parse.quote_plus(query)
    loc = urllib.parse.quote_plus(location)
    url = f"https://www.myjobmag.co.ke/search/jobs?q={q}&location={loc}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=['--deny-permission-prompts', '--disable-notifications']
        )
        page = await browser.new_page()
        await page.goto(url, wait_until='networkidle')

        try:
            no_thanks = page.locator("text=NO THANKS")
            if await no_thanks.is_visible(timeout=3000):
                await no_thanks.click()
        except Exception:
            pass

        await page.wait_for_selector('ul.job-list', timeout=10000)
        job_listings = await page.query_selector_all('ul.job-list > li.job-list-li')

        scraped_jobs = []
        scrape_time = datetime.now().isoformat(timespec="seconds")
        print(f"Scraped {scrape_time} job listings from the page")

        for job in job_listings:
            if await job.query_selector('#adbox'):
                continue

            title_el = await job.query_selector('.mag-b h2 a')
            title = (await title_el.inner_text()).strip() if title_el else ""
            job_url = (await title_el.get_attribute('href')) if title_el else ""

            company_el = await job.query_selector('.job-logo img')
            company = (await company_el.get_attribute('alt') or "").strip() if company_el else ""

            date_el = await job.query_selector('#job-date')
            date_posted = (await date_el.inner_text()).strip() if date_el else ""

            desc_el = await job.query_selector('.job-desc')
            desc = (await desc_el.inner_text()).strip() if desc_el else ""

            if title and job_url:
                scraped_jobs.append({
                    "job_url": job_url,
                    "title": title,
                    "company": company,
                    "date_posted": date_posted,
                    "description": desc,
                    "scraped_at": scrape_time,
                })

        await browser.close()
        return scraped_jobs


async def main():
    jobs = await scrape_myjobmag("software engineering", "Nairobi")
    print(f"Scraped {len(jobs)} job listings from the page")

    existing_urls = load_existing_urls(CSV_FILE)
    new_count = append_jobs_to_csv(CSV_FILE, jobs, existing_urls)

    print(f"Added {new_count} new listings to {CSV_FILE}")
    print(f"Skipped {len(jobs) - new_count} duplicates already saved")


if __name__ == '__main__':
    asyncio.run(main())