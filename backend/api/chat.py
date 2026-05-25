# =============================================
# Chat API Router
# POST /api/chat      — standard response
# GET  /api/chat/stream — SSE streaming
# =============================================

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from loguru import logger

from vectordb.store import query_similar
from llm.claude_client import chat, stream_chat

router = APIRouter()


class ChatRequest(BaseModel):
    """Request body for the chat endpoint."""
    question: str
    history: list[dict] = []  # optional conversation history


class ChatResponse(BaseModel):
    """Response body from the chat endpoint."""
    answer: str
    sources: list[str]  # list of source URLs used to answer


@router.post("", response_model=ChatResponse)
async def ask(req: ChatRequest):
    """
    Main chat endpoint.
    1. Embed the question
    2. Retrieve top-5 similar chunks from ChromaDB
    3. Send question + context to Claude
    4. Return answer + source URLs
    """
    logger.info(f"Question: {req.question[:80]}")

    # Retrieve the most relevant CSU content for this question
    context_chunks = query_similar(req.question, n_results=5)

    # Get Claude's answer using the retrieved context
    answer = chat(req.question, context_chunks, req.history)

    # Deduplicate and return source URLs
    sources = list(dict.fromkeys(c["url"] for c in context_chunks))

    return ChatResponse(answer=answer, sources=sources)


@router.get("/stream")
async def stream(question: str, history: str = "[]"):
    """
    Streaming chat endpoint using Server-Sent Events (SSE).
    The Next.js frontend reads this as a ReadableStream.
    """
    import json

    context_chunks = query_similar(question, n_results=5)

    async def event_generator():
        # Stream each token as an SSE data event
        async for token in stream_chat(question, context_chunks):
            yield f"data: {json.dumps({'token': token})}\n\n"

        # Signal the frontend that streaming is complete
        sources = list(dict.fromkeys(c["url"] for c in context_chunks))
        yield f"data: {json.dumps({'done': True, 'sources': sources})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )
