import streamlit as st
import requests
import uuid

# --- Page config ---
# This must be the first Streamlit call in the script.
# Sets the browser tab title and layout.
st.set_page_config(
    page_title="Telemetry Query Agent",
    page_icon="📡",
    layout="centered"
)

# --- Constants ---
API_URL = "http://localhost:8000/api"

# --- Session state ---
# Streamlit reruns the whole script on every interaction.
# st.session_state is how you persist values across reruns —
# think of it like a ViewModel in Android that survives
# configuration changes.
if "session_id" not in st.session_state:
    # Generate a unique session ID for this browser session
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    # List of {"role": "user"|"assistant", "content": "..."}
    st.session_state.messages = []

if "sources" not in st.session_state:
    st.session_state.sources = []


# --- Helper functions ---
def send_message(message: str) -> dict:
    """
    Calls your FastAPI backend and returns the response.
    If the server is down, returns a friendly error dict.
    """
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={
                "message": message,
                "session_id": st.session_state.session_id
            },
            timeout=30  # Agent can take a few seconds — give it time
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {
            "answer": "⚠️ Could not reach the backend. Is your FastAPI server running on port 8000?",
            "sources": []
        }
    except Exception as e:
        return {
            "answer": f"⚠️ Something went wrong: {str(e)}",
            "sources": []
        }


def clear_conversation():
    """
    Clears chat history locally and on the backend.
    """
    try:
        requests.delete(f"{API_URL}/sessions/{st.session_state.session_id}")
    except Exception:
        pass  # If backend is unreachable, still clear locally

    st.session_state.messages = []
    st.session_state.sources = []
    st.session_state.session_id = str(uuid.uuid4())  # Fresh session


# --- UI ---

# Header
st.title("📡 Telemetry Query Agent")
st.caption("Ask anything about Android and iOS telemetry APIs")

# Platform filter — purely cosmetic for now,
# you can wire this to the backend in a future iteration
platform = st.radio(
    "Focus on:",
    ["Both", "Android", "iOS"],
    horizontal=True
)

st.divider()

# --- Chat history ---
# Loop through all past messages and render them.
# Streamlit's st.chat_message gives you the
# bubble UI automatically.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Sources from last response ---
if st.session_state.sources:
    with st.expander("📚 Sources used in last answer"):
        for source in st.session_state.sources:
            st.markdown(f"- {source}")

# --- Chat input ---
# st.chat_input sticks to the bottom of the screen.
# It returns the user's message when they hit Enter,
# or None if they haven't typed anything yet.
if prompt := st.chat_input("e.g. How do I detect ANR on Android?"):

    # 1. Show user message immediately
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Call backend and show a spinner while waiting
    with st.chat_message("assistant"):
        with st.spinner("Searching docs and thinking..."):
            response = send_message(prompt)

        answer = response.get("answer", "No answer returned.")
        sources = response.get("sources", [])

        st.markdown(answer)

    # 3. Save assistant message and sources to session state
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
    st.session_state.sources = sources

    # 4. Rerun so the sources expander updates immediately
    st.rerun()

# --- Sidebar ---
with st.sidebar:
    st.header("Session")
    st.caption(f"ID: `{st.session_state.session_id[:8]}...`")

    if st.button("🗑️ New conversation", use_container_width=True):
        clear_conversation()
        st.rerun()

    st.divider()
    st.header("About")
    st.markdown("""
        This agent searches real Android and iOS
        telemetry documentation to answer your questions.

        **Powered by:**
        - OpenAI GPT-4o-mini
        - LangChain agent loop
        - ChromaDB vector search
        - FastAPI backend
        - Streamlit frontend
    """)
