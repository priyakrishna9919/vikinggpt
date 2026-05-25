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

# Track scrape status in memory
scrape_status = {"running": False, "last_run": None, "pages_scraped": 0, "error": None}


def run_full_pipeline():
    """
    Full scrape + embed + ingest pipeline.
    Runs in a background task — logs all errors explicitly.
    """
    global scrape_status
    scrape_status["running"] = True
    scrape_status["error"] = None
    logger.info("Starting CSU scrape pipeline...")

    try:
        # Step 1: Scrape CSU pages with Playwright
        logger.info("Step 1: Launching Playwright scraper...")
        pages = run_scraper()
        logger.info(f"Step 1 done — scraped {len(pages)} pages")

        # Step 2: Chunk, embed, and store in ChromaDB
        logger.info("Step 2: Embedding and ingesting into ChromaDB...")
        ingest_pages(pages)
        logger.info("Step 2 done — ingestion complete")

        scrape_status["pages_scraped"] = len(pages)
        scrape_status["last_run"] = datetime.utcnow().isoformat()
        logger.info(f"Pipeline complete — {len(pages)} pages ingested")

    except Exception as e:
        # Log the full traceback so we can see exactly what went wrong
        error_msg = traceback.format_exc()
        logger.error(f"Scrape pipeline failed:\n{error_msg}")
        scrape_status["error"] = str(e)
    finally:
        scrape_status["running"] = False


@router.post("/run")
async def trigger_scrape(background_tasks: BackgroundTasks):
    """Trigger a full scrape + ingest in the background."""
    if scrape_status["running"]:
        return {"message": "Scrape already in progress", "status": scrape_status}

    background_tasks.add_task(run_full_pipeline)
    return {"message": "Scrape started in background", "status": scrape_status}


@router.get("/status")
async def get_status():
    """Return the current scraper state including any errors."""
    return scrape_status
