# =============================================
# CSU Web Scraper — requests + BeautifulSoup
# Simpler and more reliable than Playwright
# on Windows — no async, no subprocess issues
# =============================================

import requests
from bs4 import BeautifulSoup
from loguru import logger

# All CSU pages Viking should know about
CSU_PAGES = [
    "https://www.csuohio.edu/admissions",
    "https://www.csuohio.edu/admissions/undergraduate",
    "https://www.csuohio.edu/admissions/graduate",
    "https://www.csuohio.edu/bursar/tuition-and-fees",
    "https://www.csuohio.edu/financialaid",
    "https://www.csuohio.edu/registrar/academic-calendar",
    "https://www.csuohio.edu/residence-life",
    "https://www.csuohio.edu/academics/colleges",
    "https://www.csuohio.edu/student-life",
    "https://www.csuohio.edu/contact-us",
    "https://www.csuohio.edu/career-services",
    "https://www.csuohio.edu/parking",
    "https://www.csuohio.edu/library",
    "https://www.csuohio.edu/international-services",
    "https://csurec.com",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
}


def scrape_page(url: str) -> dict:
    """
    Fetch a URL with requests and extract visible text
    using BeautifulSoup. Strips nav/footer/scripts.
    """
    try:
        logger.info(f"Scraping: {url}")
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove noisy elements before extracting text
        for tag in soup(["nav", "footer", "script", "style", "header"]):
            tag.decompose()

        # Get clean visible text
        text = soup.get_text(separator=" ", strip=True)
        cleaned = " ".join(text.split())

        return {"url": url, "text": cleaned, "success": True}

    except Exception as e:
        logger.error(f"Failed to scrape {url}: {e}")
        return {"url": url, "text": "", "success": False}


def run_scraper() -> list[dict]:
    """
    Scrape all CSU pages and return a list of
    {url, text} dicts for pages with content.
    """
    results = []

    for url in CSU_PAGES:
        result = scrape_page(url)
        if result["success"] and len(result["text"]) > 100:
            results.append(result)
            logger.info(f"  OK — {len(result['text'])} chars from {url}")

    logger.info(f"Scraped {len(results)}/{len(CSU_PAGES)} pages successfully")
    return results
