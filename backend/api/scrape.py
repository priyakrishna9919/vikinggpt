# =============================================
# Scrape API Router
# POST /api/scrape/run — trigger a full scrape
# GET  /api/scrape/status — check last run info
# =============================================

from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from datetime import datetime
from loguru import logger

from scraper.crawler import run_scraper
from vectordb.store import ingest_pages

router = APIRouter()

# Track scrape status in memory (use Redis in production for multi-worker)
scrape_status = {"running": False, "last_run": None, "pages_scraped": 0}


def run_full_pipeline():
    """
    Full scrape + embed + ingest pipeline.
    Runs in a background task so the API response is instant.
    """
    global scrape_status
    scrape_status["running"] = True
    logger.info("Starting CSU scrape pipeline...")

    try:
        # Step 1: Scrape all CSU pages with Playwright
        pages = run_scraper()

        # Step 2: Chunk, embed, and store in ChromaDB
        ingest_pages(pages)

        scrape_status["pages_scraped"] = len(pages)
        scrape_status["last_run"] = datetime.utcnow().isoformat()
        logger.info(f"Pipeline complete — {len(pages)} pages ingested")

    except Exception as e:
        logger.error(f"Scrape pipeline failed: {e}")
    finally:
        scrape_status["running"] = False


@router.post("/run")
async def trigger_scrape(background_tasks: BackgroundTasks):
    """
    Trigger a full scrape + ingest in the background.
    Returns immediately — check /status for progress.
    """
    if scrape_status["running"]:
        return {"message": "Scrape already in progress", "status": scrape_status}

    background_tasks.add_task(run_full_pipeline)
    return {"message": "Scrape started in background", "status": scrape_status}


@router.get("/status")
async def get_status():
    """Return the current state of the scraper."""
    return scrape_status
