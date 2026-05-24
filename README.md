# 📡 Telemetry Query Agent

An AI agent that answers questions about Android and iOS telemetry APIs,
grounded in real documentation from Android Developers and Apple Developer portals.

Built to explore RAG, AI agents, and full-stack AI development —
coming from an Android engineering background.

---

## What it does

- Answers natural language questions about mobile telemetry APIs
- Retrieves answers from real Android/iOS documentation (not LLM memory)
- Maintains conversation history across follow-up questions
- Cites the source docs used in each answer
- Handles platform-specific queries (Android only, iOS only, or both)

---

## Architecture

```
Streamlit UI  →  FastAPI backend  →  LangChain agent loop
                                          ↓
                                   ChromaDB (vector search)
                                          ↓
                              Android + iOS doc chunks
```

**Stack:**
- Frontend: Streamlit
- Backend: FastAPI + Python
- Agent framework: LangChain
- LLM: GPT-4o-mini
- Vector DB: ChromaDB
- Embeddings: OpenAI text-embedding-3-small

---

## Getting started

### Prerequisites
- Python 3.11+
- An OpenAI API key ([get one here](https://platform.openai.com))

### 1. Clone and set up environment

```bash
git clone https://github.com/your-username/your-repo-name
cd your-repo-name/backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Open .env and add your OpenAI API key
```

### 3. Ingest documentation

This fetches Android and iOS telemetry docs, chunks them,
and stores embeddings in a local ChromaDB instance.
Run this once before starting the server.

```bash
python ingest_run.py
```

### 4. Start the backend

```bash
uvicorn main:app --reload --port 8000
```

API docs available at: `http://localhost:8000/docs`

### 5. Start the frontend

Open a new terminal:

```bash
cd frontend
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## Example questions to try

- *What is ANR and how does Android detect it?*
- *How do I monitor battery usage on Android?*
- *What does MetricKit provide on iOS?*
- *Compare how Android and iOS handle performance monitoring*
- *How do I track app startup time on iOS?*

---

## Project structure

```
├── backend/
│   ├── agent/
│   │   ├── agent.py        # LangChain agent + prompt
│   │   └── tools.py        # Tools the agent can call
│   ├── api/
│   │   ├── models.py       # Request/response schemas
│   │   └── routes.py       # FastAPI endpoints
│   ├── ingest/
│   │   ├── scraper.py      # Fetches doc pages
│   │   └── pipeline.py     # Chunks, embeds, stores
│   ├── main.py             # FastAPI app entry point
│   ├── ingest_run.py       # Run once to populate vector DB
│   └── requirements.txt
├── frontend/
│   └── app.py              # Streamlit chat UI
└── README.md
```

---

## How it works

1. **Ingestion** — Android and iOS telemetry doc pages are scraped,
   split into ~500 token chunks, embedded via OpenAI, and stored in ChromaDB

2. **Query** — when a user asks a question, it's embedded using the same model
   and compared against stored chunks via cosine similarity search

3. **Agent loop** — a LangChain agent decides which tool to call
   (broad search, platform-filtered search, or code example),
   retrieves relevant chunks, and passes them to GPT-4o-mini

4. **Answer** — the LLM generates a response grounded in the retrieved docs,
   with source citations returned to the frontend

---

## What to say in interviews

> "I built a domain-specific AI agent that helps mobile developers query Android and iOS telemetry APIs in natural language. The challenge was making sure answers were grounded in real documentation rather than LLM hallucinations — so I built a RAG pipeline that ingests real dev docs, chunks and embeds them into a vector database, and retrieves the most relevant chunks before the LLM ever sees the question. On top of that I added an agent loop with multiple tools so it can handle follow-up questions, platform-specific queries, and code examples — all through a chat interface backed by a FastAPI REST API."

---

## Extending the project

Add more documentation sources by editing `DOC_SOURCES` in `backend/ingest/scraper.py`:

```python
{
    "url": "https://firebase.google.com/docs/perf-mon",
    "platform": "android",
    "topic": "Firebase Performance Monitoring"
},
```

Then re-run `python ingest_run.py` to rebuild the vector database.
