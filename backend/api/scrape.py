# =============================================
# Scrape API Router
# POST /api/scrape/run — trigger a full scrape
# GET  /api/scrape/status — check last run info
#
# Fix: Playwright can't run in FastAPI's async
# event loop on Windows — use a thread instead
# =============================================

from fastapi import APIRouter, BackgroundTasks
from datetime import datetime
from loguru import logger
import traceback
import asyncio
import concurrent.futures

from scraper.crawler import run_scraper
from vectordb.store import ingest_pages

router = APIRouter()

scrape_status = {"running": False, "last_run": None, "pages_scraped": 0, "error": None}


def run_full_pipeline():
    """
    Runs the full scrape + embed + ingest pipeline.
    Called inside a ThreadPoolExecutor so Playwright
    can create its own event loop without conflicting
    with FastAPI's event loop (Windows fix).
    """
    global scrape_status
    scrape_status["running"] = True
    scrape_status["error"] = None
    logger.info("Starting CSU scrape pipeline in thread...")

    try:
        # Playwright needs its own event loop — create one in this thread
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        logger.info("Step 1: Launching Playwright scraper...")
        pages = run_scraper()
        logger.info(f"Step 1 done — scraped {len(pages)} pages")

        logger.info("Step 2: Embedding and ingesting into ChromaDB...")
        ingest_pages(pages)
        logger.info("Step 2 complete")

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
async def trigger_scrape():
    """
    Trigger a full scrape + ingest.
    Runs in a thread pool so Playwright works on Windows.
    Returns immediately — poll /status for progress.
    """
    if scrape_status["running"]:
        return {"message": "Scrape already in progress", "status": scrape_status}

    # Run in a separate thread — fixes Windows asyncio + Playwright conflict
    loop = asyncio.get_event_loop()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    loop.run_in_executor(executor, run_full_pipeline)

    return {"message": "Scrape started in thread", "status": scrape_status}


@router.get("/status")
async def get_status():
    """Return current scraper state."""
    return scrape_status
