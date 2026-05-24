from fastapi import APIRouter, HTTPException
from langchain.schema import HumanMessage, AIMessage

from agent.agent import build_agent
from api.models import ChatRequest, ChatResponse

router = APIRouter()

# --- Agent instance ---
# We build the agent once when the server starts, not on
# every request. Rebuilding it each time would be slow
# and wasteful — same idea as a singleton in Android.
print("Initialising agent...")
agent = build_agent()
print("Agent ready.")

# --- Conversation memory ---
# A simple dictionary mapping session_id → list of messages.
# In production you'd use Redis or a database, but for a
# portfolio project an in-memory dict is perfectly fine.
# Structure: { "session_id": [HumanMessage(...), AIMessage(...), ...] }
conversation_history: dict[str, list] = {}


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint.
    Accepts a message + session_id, runs the agent,
    returns the answer with sources.
    """
    try:
        # Get or create history for this session
        history = conversation_history.get(request.session_id, [])

        # Run the agent with the full conversation history.
        # This is what gives the agent memory — it sees all
        # previous messages, not just the current one.
        result = agent.invoke({
            "input": request.message,
            "chat_history": history,
        })

        answer = result["output"]

        # Update history with this turn.
        # HumanMessage = user's message, AIMessage = agent's reply.
        history.append(HumanMessage(content=request.message))
        history.append(AIMessage(content=answer))
        conversation_history[request.session_id] = history

        # Extract source citations from the agent's intermediate steps.
        # intermediate_steps contains the raw tool call results —
        # we dig into them to pull out the metadata topics.
        sources = []
        for step in result.get("intermediate_steps", []):
            # Each step is a tuple: (tool_action, tool_output_string)
            tool_output = step[1] if len(step) > 1 else ""
            # Our tool output format includes [PLATFORM — Topic] headers
            # so we extract those lines as source citations
            for line in tool_output.split("\n"):
                if line.startswith("[") and "—" in line:
                    source = line.strip("[]")
                    if source not in sources:
                        sources.append(source)

        return ChatResponse(
            answer=answer,
            session_id=request.session_id,
            sources=sources,
        )

    except Exception as e:
        # Always wrap agent calls in try/except —
        # LLM APIs can timeout or return unexpected errors
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/sessions/{session_id}")
async def clear_session(session_id: str):
    """
    Clears conversation history for a session.
    Useful for a 'New conversation' button in the frontend.
    """
    if session_id in conversation_history:
        del conversation_history[session_id]
    return {"message": f"Session {session_id} cleared"}


@router.get("/health")
async def health():
    """
    Simple health check endpoint.
    Lets you verify the server is running.
    """
    return {"status": "ok"}
