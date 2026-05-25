# VikingGPT — Cleveland State University AI Assistant

A BearcatGPT-style AI assistant for CSU students. Built with a production-grade RAG pipeline that scrapes csuohio.edu, embeds the content, and answers questions using Claude.

## Architecture

| Layer      | Stack                        |
|------------|------------------------------|
| Frontend   | Next.js 14 + Tailwind CSS    |
| Backend    | FastAPI + Uvicorn            |
| Scraping   | Playwright (headless Chrome) |
| Embeddings | OpenAI text-embedding-3-small|
| Vector DB  | ChromaDB (persistent)        |
| LLM        | Claude (claude-sonnet-4)     |
| Deployment | Railway (API) + Vercel (UI)  |

## How It Works

1. **Scrape** — Playwright crawls csuohio.edu pages (admissions, tuition, housing, rec center, etc.)
2. **Chunk** — Text is split into 500-word overlapping chunks
3. **Embed** — OpenAI generates vector embeddings for each chunk
4. **Store** — Embeddings are stored in ChromaDB with source URLs
5. **Query** — User question is embedded and top-5 similar chunks are retrieved
6. **Generate** — Claude answers using the retrieved context (RAG)
7. **Stream** — Response is streamed token-by-token to the Next.js frontend

## Project Structure

```
vikinggpt/
├── frontend/               # Next.js app (Vercel)
│   ├── app/
│   │   ├── chat/page.tsx   # Main chat interface
│   │   └── layout.tsx
│   ├── components/
│   │   ├── Sidebar.tsx     # CSU green sidebar
│   │   ├── AgentCards.tsx  # Home view agent grid
│   │   └── ChatMessage.tsx # Message bubbles
│   └── package.json
│
└── backend/                # FastAPI server (Railway)
    ├── main.py             # Entry point, CORS, routers
    ├── scraper/
    │   └── crawler.py      # Playwright CSU scraper
    ├── embeddings/
    │   ├── chunker.py      # Text chunking
    │   └── embedder.py     # OpenAI embeddings
    ├── vectordb/
    │   └── store.py        # ChromaDB operations
    ├── llm/
    │   └── claude_client.py# Claude streaming client
    ├── api/
    │   ├── chat.py         # /api/chat endpoints
    │   ├── scrape.py       # /api/scrape endpoints
    │   └── health.py       # /api/health
    └── requirements.txt
```

## Local Setup

### Backend

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium

# Set environment variables
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY and OPENAI_API_KEY

# Start the server
uvicorn main:app --reload --port 8000
```

### Run the scraper (first time setup)

```bash
# Trigger a full scrape and ingest
curl -X POST http://localhost:8000/api/scrape/run

# Check status
curl http://localhost:8000/api/scrape/status
```

### Frontend

```bash
cd frontend

npm install

cp .env.local.example .env.local
# Edit .env.local — set NEXT_PUBLIC_API_URL=http://localhost:8000

npm run dev
# Open http://localhost:3000
```

## Deployment

### Backend → Railway
1. Push to GitHub
2. Create new Railway project → Deploy from GitHub
3. Set environment variables in Railway dashboard
4. Railway auto-deploys on every push

### Frontend → Vercel
1. Import GitHub repo in Vercel
2. Set root directory to `frontend`
3. Add `NEXT_PUBLIC_API_URL` = your Railway backend URL
4. Deploy

## API Endpoints

| Method | Endpoint            | Description                        |
|--------|---------------------|------------------------------------|
| POST   | /api/chat           | Ask a question, get full response  |
| GET    | /api/chat/stream    | Ask a question, stream response    |
| POST   | /api/scrape/run     | Trigger CSU scrape + ingest        |
| GET    | /api/scrape/status  | Check scraper status               |
| GET    | /api/health         | Health check + DB chunk count      |
