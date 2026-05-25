# =============================================
# OpenAI Embeddings
# Converts text chunks into vector embeddings
# using OpenAI text-embedding-3-small model
# =============================================

import os
from openai import OpenAI
from loguru import logger

# Initialize the OpenAI client with the API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Model to use — small is fast and cheap, good for RAG
EMBEDDING_MODEL = "text-embedding-3-small"


def embed_text(text: str) -> list[float]:
    """
    Generate a vector embedding for a single text string.
    Returns a list of floats (1536 dimensions for text-embedding-3-small).
    """
    response = client.embeddings.create(
        input=text,
        model=EMBEDDING_MODEL
    )
    return response.data[0].embedding


def embed_batch(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for a batch of text chunks.
    OpenAI allows up to 2048 inputs per request.
    We batch in groups of 100 to stay safe.
    """
    all_embeddings = []

    for i in range(0, len(texts), 100):
        batch = texts[i:i + 100]
        logger.info(f"Embedding batch {i // 100 + 1} ({len(batch)} chunks)")

        response = client.embeddings.create(
            input=batch,
            model=EMBEDDING_MODEL
        )

        # Preserve original order from the response
        batch_embeddings = [item.embedding for item in sorted(response.data, key=lambda x: x.index)]
        all_embeddings.extend(batch_embeddings)

    return all_embeddings
