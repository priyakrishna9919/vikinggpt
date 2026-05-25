# =============================================
# Scrape API Router
# POST /api/scrape/run — trigger a full scrape
# GET  /api/scrape/status — check last run info
# =============================================

from fastapi import APIRouter, BackgroundTasks
from datetime import datetime
from loguru import logger
import traceback

from scraper.crawler import run_scraper
from vectordb.store import ingest_pages

router = APIRouter()

scrape_status = {"running": False, "last_run": None, "pages_scraped": 0, "error": None}


def run_full_pipeline():
    """Full scrape + embed + ingest pipeline."""
    global scrape_status
    scrape_status["running"] = True
    scrape_status["error"] = None
    logger.info("Starting CSU scrape pipeline...")

    try:
        logger.info("Step 1: Scraping CSU pages...")
        pages = run_scraper()
        logger.info(f"Step 1 done — {len(pages)} pages scraped")

        logger.info("Step 2: Embedding and ingesting into ChromaDB...")
        ingest_pages(pages)
        logger.info("Step 2 done")

        scrape_status["pages_scraped"] = len(pages)
        scrape_status["last_run"] = datetime.utcnow().isoformat()
        logger.info(f"Pipeline complete — {len(pages)} pages ingested")

    except Exception as e:
        error_msg = traceback.format_exc()
        logger.error(f"Scrape pipeline failed:\n{error_msg}")
        scrape_status["error"] = str(e)
    finally:
        scrape_status["running"] = False


@router.post("/run")
async def trigger_scrape(background_tasks: BackgroundTasks):
    """Trigger scrape + ingest as a background task."""
    if scrape_status["running"]:
        return {"message": "Already running", "status": scrape_status}
    background_tasks.add_task(run_full_pipeline)
    return {"message": "Scrape started", "status": scrape_status}


@router.get("/status")
async def get_status():
    return scrape_status
