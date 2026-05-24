from pydantic import BaseModel
from typing import Optional

# Pydantic is Python's way of defining typed data models.
# FastAPI uses these to automatically validate incoming JSON
# and generate API documentation. Think of it like a
# Kotlin data class with built-in validation.

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"
    # session_id lets us track conversation history per user.
    # Optional means it's not required — defaults to "default"

class ChatResponse(BaseModel):
    answer: str
    session_id: str
    sources: list[str] = []
    # sources will hold the doc topics the agent retrieved —
    # these show up as citations in the frontend later
