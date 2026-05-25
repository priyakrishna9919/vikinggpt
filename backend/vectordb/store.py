# =============================================
# ChromaDB Vector Store
# Stores and retrieves CSU content embeddings
# Persisted to disk so data survives restarts
# =============================================

import os
import uuid
import chromadb
from chromadb.config import Settings
from loguru import logger

from embeddings.chunker import chunk_text
from embeddings.embedder import embed_batch

# Global ChromaDB client and collection — initialized once on startup
_client = None
_collection = None


def init_collection():
    """
    Initialize ChromaDB with a persistent storage path.
    Creates the CSU knowledge collection if it doesn't exist yet.
    """
    global _client, _collection

    persist_path = os.getenv("CHROMA_PERSIST_PATH", "./chroma_db")
    collection_name = os.getenv("CHROMA_COLLECTION", "csu_knowledge")

    # PersistentClient saves data to disk automatically
    _client = chromadb.PersistentClient(
        path=persist_path,
        settings=Settings(anonymized_telemetry=False)
    )

    # get_or_create so we don't lose data on restart
    _collection = _client.get_or_create_collection(
        name=collection_name,
        metadata={"description": "Cleveland State University knowledge base"}
    )

    count = _collection.count()
    logger.info(f"ChromaDB ready — collection '{collection_name}' has {count} chunks")


def get_collection():
    """Return the active ChromaDB collection, initializing if needed."""
    if _collection is None:
        init_collection()
    return _collection


def ingest_pages(pages: list[dict]):
    """
    Take scraped CSU pages, chunk the text, embed each chunk,
    and upsert everything into ChromaDB.

    pages: list of {url: str, text: str} dicts from the scraper
    """
    collection = get_collection()

    all_ids = []
    all_embeddings = []
    all_documents = []
    all_metadatas = []

    for page in pages:
        # Split each page into overlapping chunks
        chunks = chunk_text(page["text"])
        logger.info(f"  {page['url']} → {len(chunks)} chunks")

        for i, chunk in enumerate(chunks):
            # Unique ID: url + chunk index
            chunk_id = f"{page['url']}__chunk_{i}"
            all_ids.append(chunk_id)
            all_documents.append(chunk)
            all_metadatas.append({"url": page["url"], "chunk_index": i})

    if not all_ids:
        logger.warning("No chunks to ingest")
        return

    # Generate embeddings for all chunks in batches
    logger.info(f"Generating embeddings for {len(all_ids)} chunks...")
    all_embeddings = embed_batch(all_documents)

    # Upsert into ChromaDB — safe to run multiple times
    collection.upsert(
        ids=all_ids,
        embeddings=all_embeddings,
        documents=all_documents,
        metadatas=all_metadatas,
    )

    logger.info(f"Ingested {len(all_ids)} chunks into ChromaDB")


def query_similar(query_text: str, n_results: int = 5) -> list[dict]:
    """
    Find the most semantically similar chunks to a user query.
    Returns a list of {text, url, score} dicts ordered by relevance.
    """
    from embeddings.embedder import embed_text

    collection = get_collection()

    if collection.count() == 0:
        logger.warning("ChromaDB is empty — run /api/scrape/run first")
        return []

    # Embed the user's query to compare against stored chunks
    query_embedding = embed_text(query_text)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )

    # Format results into clean dicts
    chunks = []
    for i, doc in enumerate(results["documents"][0]):
        chunks.append({
            "text": doc,
            "url": results["metadatas"][0][i]["url"],
            "score": 1 - results["distances"][0][i],  # convert distance to similarity
        })

    return chunks
