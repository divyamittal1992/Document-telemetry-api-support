import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"  # Suppress Chroma noise

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI(
    title="Telemetry Query Agent",
    description="AI agent for querying Android and iOS telemetry APIs",
    version="1.0.0"
)

# CORS middleware — this is what allows your React frontend
# (running on localhost:3000) to talk to this server
# (running on localhost:8000) without the browser blocking it.
# Same as allowing cross-origin requests in an Android WebView.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register our routes under the /api prefix
# So /chat becomes /api/chat, /health becomes /api/health etc.
app.include_router(router, prefix="/api")
