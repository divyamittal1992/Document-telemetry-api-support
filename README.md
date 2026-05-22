# Telemetry API Support Agent

An Agentic RAG application that lets Android and iOS developers
ask questions about Telemetry API integration, answered by an AI
agent grounded in official documentation and support content.

## Problem it solves
Telemetry API documentation is spread across multiple sources —
SDK references, integration guides, troubleshooting docs, and
release notes. This agent lets developers ask natural language
questions and get accurate, sourced answers instantly instead
of hunting through docs manually.

## Architecture
[diagram coming soon]

## Tech Stack
- Frontend: React
- Backend: FastAPI (Python)
- Vector DB: Supabase + PGVector
- LLM: Claude / OpenAI
- Agent framework: LangChain

## Features
- Upload Telemetry API docs (PDF, markdown, text)
- Semantic search over documentation content
- AI agent with multi-step reasoning for complex queries
- Answers grounded in source documents — no hallucination
- Supports Android and iOS specific queries
- Streaming responses
- Auth via Supabase

## Example questions you can ask
- "How do I initialize the Telemetry SDK on Android 14?"
- "What permissions are required for telemetry on iOS 17?"
- "Why is my telemetry data not appearing in the dashboard?"
- "What changed in the Telemetry API in the latest release?"
- "How do I handle telemetry in background processes on Android?"

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Supabase account
- OpenAI or Anthropic API key

### Backend setup
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp .env.example .env         # fill in your keys
uvicorn app.main:app --reload

### Frontend setup
cd frontend
npm install
npm run dev

## Environment Variables
See `.env.example` for required variables.
Never commit your real `.env` file.

## Document Sources
The agent is trained on the following documentation:
- Telemetry SDK Android integration guide
- Telemetry SDK iOS integration guide
- API reference (REST endpoints)
- Troubleshooting and FAQ
- Release notes and changelog

## Engineering Decisions
- Paragraph-level chunking over full-page chunking
  for better retrieval precision
- Separate collections for Android and iOS docs
  so the agent can filter by platform when relevant
- ReAct agent pattern for multi-step queries
  that need to cross-reference multiple doc sections

## What I learned
[Fill this in as you build — this section is gold in interviews]

## Roadmap
- [ ] Basic RAG pipeline
- [ ] Agent layer with multi-step reasoning
- [ ] FastAPI backend
- [ ] React chat UI
- [ ] Platform filter (Android / iOS toggle)
- [ ] Deploy to production