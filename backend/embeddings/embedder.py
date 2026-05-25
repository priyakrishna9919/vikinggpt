# =============================================
# Local Embeddings — sentence-transformers
# Runs 100% locally, no API key, no cost
# Uses all-MiniLM-L6-v2 — fast, accurate,
# great for RAG on short/medium text chunks
# =============================================

from sentence_transformers import SentenceTransformer
from loguru import logger

# Load the model once at module level so it's not reloaded on every call
# Downloads automatically on first run (~90MB), cached after that
MODEL_NAME = "all-MiniLM-L6-v2"
_model = None


def get_model() -> SentenceTransformer:
    """Lazy-load the model — only downloads on first call."""
    global _model
    if _model is None:
        logger.info(f"Loading embedding model: {MODEL_NAME}")
        _model = SentenceTransformer(MODEL_NAME)
        logger.info("Embedding model loaded")
    return _model


def embed_text(text: str) -> list[float]:
    """
    Generate a vector embedding for a single text string.
    Returns a list of floats (384 dimensions for MiniLM).
    """
    model = get_model()
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()


def embed_batch(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for a list of text chunks in one pass.
    sentence-transformers handles batching internally — fast and efficient.
    """
    model = get_model()
    logger.info(f"Embedding {len(texts)} chunks locally...")
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
    return [e.tolist() for e in embeddings]
