# =============================================
# CSU Web Scraper — requests + BeautifulSoup
# Updated with full URL list including
# registrar, viking vets, enrollment pages
# =============================================

import requests
from bs4 import BeautifulSoup
from loguru import logger

CSU_PAGES = [
    # ── ADMISSIONS ──
    "https://www.csuohio.edu/admissions",
    "https://www.csuohio.edu/admissions/undergraduate",
    "https://www.csuohio.edu/admissions/graduate",
    "https://csuohio.edu/admissions/enroll",

    # ── TUITION & FINANCIAL AID ──
    "https://www.csuohio.edu/bursar/tuition-and-fees",
    "https://www.csuohio.edu/financialaid",

    # ── REGISTRAR — ENROLLMENT ──
    "https://www.csuohio.edu/registrar",
    "https://www.csuohio.edu/registrar/academic-calendar",
    "https://www.csuohio.edu/registrar/academic-year-registration-information",
    "https://www.csuohio.edu/registrar/register-for-classes",
    "https://www.csuohio.edu/registrar/how-enroll",
    "https://www.csuohio.edu/registrar/multi-term-registration",
    "https://www.csuohio.edu/registrar/registration-holds",
    "https://www.csuohio.edu/registrar/enrollment-and-degree-verification",
    "https://www.csuohio.edu/registrar/checklist-for-students-not-attending",
    "https://www.csuohio.edu/registrar/ohio-residency",
    "https://www.csuohio.edu/registrar/non-degree-student-information",
    "https://www.csuohio.edu/registrar/guest-student-information",
    "https://www.csuohio.edu/registrar/cross-registration",
    "https://www.csuohio.edu/registrar/transient-student-information",

    # ── REGISTRAR — GRADES & STANDING ──
    "https://www.csuohio.edu/registrar/grading-information",
    "https://www.csuohio.edu/registrar/grade-point-average",
    "https://www.csuohio.edu/registrar/grades",
    "https://www.csuohio.edu/registrar/incomplete-grades",
    "https://www.csuohio.edu/registrar/undergraduate-course-repeat-policy",
    "https://www.csuohio.edu/registrar/taking-courses-satisfactory-or-unsatisfactory",
    "https://www.csuohio.edu/registrar/taking-courses-audit-basis",
    "https://www.csuohio.edu/registrar/undergraduate-students-taking-graduate-courses",
    "https://www.csuohio.edu/registrar/undergraduate-academic-standing-policy-faq",

    # ── REGISTRAR — GRADUATION ──
    "https://www.csuohio.edu/registrar/graduation-application-deadlines",
    "https://www.csuohio.edu/registrar/undergraduate-applicants",
    "https://www.csuohio.edu/registrar/graduate-applicants",
    "https://www.csuohio.edu/registrar/diploma-information",
    "https://www.csuohio.edu/registrar/commencement-exceptions",
    "https://www.csuohio.edu/registrar/degree-audit",

    # ── REGISTRAR — TRANSCRIPTS & RECORDS ──
    "https://www.csuohio.edu/registrar/transcripts",
    "https://www.csuohio.edu/registrar/frequently-asked-questions-transcripts",
    "https://www.csuohio.edu/registrar/external-test-credit",
    "https://www.csuohio.edu/registrar/family-educational-rights-and-privacy-act",
    "https://www.csuohio.edu/registrar/university-registrar-forms",

    # ── TRANSFER ──
    "https://www.csuohio.edu/transfer-guides",
    "https://www.csuohio.edu/transfercenter",

    # ── VIKING VETS (MILITARY STUDENTS) ──
    "https://www.csuohio.edu/vikingvets/new-incoming-students",
    "https://www.csuohio.edu/vikingvets/militarytransfer-credit",
    "https://www.csuohio.edu/vikingvets/educational-benefits",
    "https://www.csuohio.edu/vikingvets/certification-process",
    "https://www.csuohio.edu/vikingvets/vmssc-orientation-0",
    "https://www.csuohio.edu/vikingvets/partnering-for-military-student-success",
    "https://www.csuohio.edu/vikingvets/student-orgs",
    "https://www.csuohio.edu/vikingvets/viking-vets-mentorship-program",
    "https://www.csuohio.edu/vikingvets/va-work-study-allowance-application",
    "https://www.csuohio.edu/vikingvets/events",
    "https://www.csuohio.edu/vikingvets/survey-and-enrollment-data",

    # ── STUDENT SERVICES ──
    "https://www.csuohio.edu/residence-life",
    "https://www.csuohio.edu/academics/colleges",
    "https://www.csuohio.edu/student-life",
    "https://www.csuohio.edu/contact-us",
    "https://www.csuohio.edu/parking",
    "https://www.csuohio.edu/all-in-1",
    "https://www.csuohio.edu/sbs",
    "https://www.csuohio.edu/international-services",
    "https://www.csuohio.edu/project60/course-enrollment",

    # ── REC CENTER ──
    "https://csurec.com",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
}


def scrape_page(url: str) -> dict:
    """Fetch a URL and extract clean visible text using BeautifulSoup."""
    try:
        logger.info(f"Scraping: {url}")
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["nav", "footer", "script", "style", "header"]):
            tag.decompose()
        text = " ".join(soup.get_text(separator=" ", strip=True).split())
        return {"url": url, "text": text, "success": True}
    except Exception as e:
        logger.error(f"Failed {url}: {e}")
        return {"url": url, "text": "", "success": False}


def run_scraper() -> list[dict]:
    """Scrape all CSU pages and return pages with content."""
    results = []
    for url in CSU_PAGES:
        r = scrape_page(url)
        if r["success"] and len(r["text"]) > 100:
            results.append(r)
            logger.info(f"  OK — {len(r['text'])} chars")
    logger.info(f"Scraped {len(results)}/{len(CSU_PAGES)} pages successfully")
    return results
