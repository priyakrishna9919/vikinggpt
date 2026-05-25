# =============================================
# Claude LLM Client
# Sends user questions + retrieved CSU context
# to Claude and streams back the response
# =============================================

import os
import anthropic
from loguru import logger

# Initialize Anthropic client with API key from environment
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

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
    Build the user message by combining the question with
    the most relevant CSU content chunks retrieved from ChromaDB.
    """
    if not context_chunks:
        return f"Question: {question}\n\nNote: No relevant CSU content was found in the knowledge base."

    # Format each chunk with its source URL
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
    Send a question + context to Claude and return the full response.
    history: list of {role, content} dicts for multi-turn conversations.
    """
    messages = history or []

    # Add the current question with retrieved context
    messages.append({
        "role": "user",
        "content": build_prompt(question, context_chunks)
    })

    logger.info(f"Calling Claude with {len(context_chunks)} context chunks")

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages,
    )

    return response.content[0].text


async def stream_chat(question: str, context_chunks: list[dict], history: list[dict] = None):
    """
    Async generator that streams Claude's response token by token.
    Used by the /api/chat/stream endpoint for real-time UI updates.
    """
    messages = history or []
    messages.append({
        "role": "user",
        "content": build_prompt(question, context_chunks)
    })

    logger.info(f"Streaming Claude response for: {question[:60]}...")

    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text
