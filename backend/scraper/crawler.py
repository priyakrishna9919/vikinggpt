# =============================================
# CSU Web Scraper — Playwright
# Crawls csuohio.edu pages, extracts clean text
# Playwright handles JS-rendered pages that
# requests/BeautifulSoup cannot reach
# =============================================

import asyncio
from playwright.async_api import async_playwright
from loguru import logger

# All CSU pages Viking should know about
CSU_PAGES = [
    "https://www.csuohio.edu/admissions",
    "https://www.csuohio.edu/bursar/tuition-and-fees",
    "https://www.csuohio.edu/registrar/academic-calendar",
    "https://www.csuohio.edu/residence-life",
    "https://www.csuohio.edu/financialaid",
    "https://www.csuohio.edu/academics/colleges",
    "https://csurec.com",
    "https://www.csuohio.edu/admissions/graduate",
    "https://www.csuohio.edu/international-services",
    "https://www.csuohio.edu/parking",
    "https://www.csuohio.edu/student-life",
    "https://www.csuohio.edu/contact-us",
    "https://www.csuohio.edu/career-services",
    "https://www.csuohio.edu/library",
]


async def scrape_page(page, url: str) -> dict:
    """Navigate to URL and extract visible text, stripping nav/footer/scripts."""
    try:
        logger.info(f"Scraping: {url}")
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(2000)

        text = await page.evaluate("""
            () => {
                ['nav','footer','script','style','header','.breadcrumb']
                    .forEach(s => document.querySelectorAll(s)
                    .forEach(e => e.remove()));
                return document.body.innerText;
            }
        """)
        return {"url": url, "text": " ".join(text.split()), "success": True}
    except Exception as e:
        logger.error(f"Failed {url}: {e}")
        return {"url": url, "text": "", "success": False}


async def scrape_all_pages() -> list[dict]:
    """Launch headless Chromium and crawl all CSU_PAGES."""
    results = []
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        ctx = await browser.new_context(user_agent="Mozilla/5.0 (compatible; VikingGPT/1.0)")
        page = await ctx.new_page()
        for url in CSU_PAGES:
            r = await scrape_page(page, url)
            if r["success"] and len(r["text"]) > 100:
                results.append(r)
        await browser.close()
    logger.info(f"Scraped {len(results)}/{len(CSU_PAGES)} pages")
    return results


def run_scraper() -> list[dict]:
    """Sync wrapper for non-async callers (scheduler, startup)."""
    return asyncio.run(scrape_all_pages())
