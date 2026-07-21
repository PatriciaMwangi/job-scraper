import asyncio
import urllib.parse
from playwright.async_api import async_playwright

async def scrape_brightermonday(location="Nairobi", job_function="Engineering", industry="", experience=""):
    """Scrape jobs from BrighterMonday"""
    a = urllib.parse.quote_plus(job_function)
    i = urllib.parse.quote_plus(industry)
    e = urllib.parse.quote_plus(experience)
    loc = urllib.parse.quote_plus(location)
    
    url = f"https://www.brightermonday.co.ke/jobs/{a}?industry={i}&location={loc}&experience={e}"
    print(f"🔍 Scraping BrighterMonday: {url}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url, wait_until='networkidle')
        
        # Wait for job listings
        await page.wait_for_selector('[data-cy="listing-title-link"]', timeout=10000)
        
        job_cards = await page.query_selector_all('.flex.flex-grow-0.flex-shrink-0.w-full')
        results = []
        
        for card in job_cards:
            try:
                title_el = await card.query_selector('a[data-cy="listing-title-link"] p.text-lg')
                title = await title_el.inner_text() if title_el else "N/A"
                
                company_el = await card.query_selector('p.text-sm.text-blue-700.text-loading-animate.inline-block.mt-3')
                company = await company_el.inner_text() if company_el else "N/A"
                
                location_el = await card.query_selector('.bg-brand-secondary-100.mr-2:first-child')
                location = await location_el.inner_text() if location_el else "N/A"
                
                results.append({
                    'title': title.strip(),
                    'company': company.strip(),
                    'location': location.strip(),
                    'source': 'BrighterMonday'
                })
                print(f"✅ {title} | {company} | {location}")
            except Exception as e:
                print(f"⚠️ Error: {e}")
                continue
        
        await browser.close()
        return results
    
if __name__ == '__main__':
    asyncio.run(scrape_brightermonday())   

