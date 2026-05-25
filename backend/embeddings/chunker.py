# =============================================
# Text Chunker
# Splits long scraped pages into smaller chunks
# so each chunk fits in one embedding call
# =============================================

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split text into overlapping word-level chunks.
    Overlap ensures context isn't lost at chunk boundaries.
    """
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        # Move forward by chunk_size minus overlap
        start += chunk_size - overlap

    return chunks
