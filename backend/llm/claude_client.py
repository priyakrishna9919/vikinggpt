# =============================================
# VikingGPT LLM Client — Groq (Llama 3)
# Free tier, no card needed
# Sign up at console.groq.com → get API key
# =============================================

import os
import httpx
import json
from loguru import logger

# Groq API endpoint
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Groq API key from environment
GROQ_API_KEY = lambda: os.getenv("GROQ_API_KEY")

# Using Llama 3.3 70B — free, fast, very capable
MODEL = "llama-3.3-70b-versatile"

# System prompt — defines Viking's personality and constraints
SYSTEM_PROMPT = """You are VikingGPT, the official AI assistant for Cleveland State University (CSU).

You answer questions using ONLY the context provided from csuohio.edu.
If the context doesn't contain the answer, say so clearly and suggest the student
contact the relevant CSU office directly.

Guidelines:
- Be helpful, accurate, and concise
- Include specific details: hours, deadlines, phone numbers, emails
- Cite the source URL when relevant
- Never make up information not in the context
- Respond in a friendly, student-advisor tone"""


def build_prompt(question: str, context_chunks: list[dict]) -> str:
    """
    Combine the user's question with retrieved CSU content chunks
    so the LLM can answer based on real csuohio.edu data.
    """
    if not context_chunks:
        return f"Question: {question}\n\nNote: No relevant CSU content was found in the knowledge base."

    context_text = "\n\n---\n\n".join([
        f"Source: {chunk['url']}\n{chunk['text']}"
        for chunk in context_chunks
    ])

    return f"""Use the following CSU content to answer the question.

CONTEXT FROM csuohio.edu:
{context_text}

QUESTION: {question}

Answer based only on the context above."""


def chat(question: str, context_chunks: list[dict], history: list[dict] = None) -> str:
    """
    Send question + context to Groq and return the full response.
    Uses the synchronous httpx client.
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Include prior conversation turns for multi-turn support
    if history:
        messages.extend(history)

    messages.append({"role": "user", "content": build_prompt(question, context_chunks)})

    logger.info(f"Calling Groq ({MODEL}) with {len(context_chunks)} context chunks")

    response = httpx.post(
        GROQ_API_URL,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY()}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": messages,
            "max_tokens": 1024,
            "temperature": 0.3,
        },
        timeout=30,
    )

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


async def stream_chat(question: str, context_chunks: list[dict], history: list[dict] = None):
    """
    Async generator that streams Groq's response token by token.
    Used by the /api/chat/stream endpoint for real-time UI updates.
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if history:
        messages.extend(history)

    messages.append({"role": "user", "content": build_prompt(question, context_chunks)})

    logger.info(f"Streaming Groq response for: {question[:60]}...")

    async with httpx.AsyncClient(timeout=60) as client:
        async with client.stream(
            "POST",
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY()}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "messages": messages,
                "max_tokens": 1024,
                "temperature": 0.3,
                "stream": True,
            },
        ) as response:
            # Read the SSE stream line by line
            async for line in response.aiter_lines():
                if not line.startswith("data: "):
                    continue

                data = line[6:]  # strip "data: " prefix

                # Stream ends with [DONE]
                if data.strip() == "[DONE]":
                    break

                try:
                    chunk = json.loads(data)
                    delta = chunk["choices"][0]["delta"].get("content", "")
                    if delta:
                        yield delta
                except (json.JSONDecodeError, KeyError):
                    continue
