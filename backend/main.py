# =============================================
# VikingGPT — FastAPI Entry Point
# Mounts all routers and starts the server
# =============================================

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from loguru import logger

from api.chat import router as chat_router
from api.scrape import router as scrape_router
from api.health import router as health_router
from vectordb.store import init_collection

# Load environment variables from .env file
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs on startup and shutdown.
    Initializes ChromaDB collection when the server starts.
    """
    logger.info("VikingGPT backend starting up...")
    init_collection()
    logger.info("ChromaDB collection initialized")
    yield
    logger.info("VikingGPT backend shutting down")


# Create the FastAPI app with lifespan handler
app = FastAPI(
    title="VikingGPT API",
    description="Cleveland State University AI assistant backend",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow requests from the Next.js frontend (local + Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(chat_router,   prefix="/api/chat",   tags=["Chat"])
app.include_router(scrape_router, prefix="/api/scrape", tags=["Scraper"])
app.include_router(health_router, prefix="/api/health", tags=["Health"])
