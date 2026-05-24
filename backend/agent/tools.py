from langchain.tools import tool
from ingest.pipeline import load_vector_store

# Load the vector store once when this module is imported.
# We don't want to reload it on every single tool call.
vector_store = load_vector_store()


@tool
def search_docs(query: str) -> str:
    """
    Search the Android and iOS telemetry documentation.
    Use this when the user asks about any telemetry API,
    metric, crash reporting, ANR, battery, performance,
    or anything related to mobile observability.
    Input should be a clear search query string.
    """
    results = vector_store.similarity_search(query, k=4)

    if not results:
        return "No relevant documentation found."

    # Format the chunks into a readable string for the LLM.
    # We include the source metadata so the LLM can cite it.
    formatted = []
    for i, chunk in enumerate(results):
        source = f"[{chunk.metadata['platform'].upper()} — {chunk.metadata['topic']}]"
        formatted.append(f"{source}\n{chunk.page_content}")

    return "\n\n---\n\n".join(formatted)


@tool
def search_docs_by_platform(query: str, platform: str) -> str:
    """
    Search telemetry documentation filtered to a specific platform.
    Use this when the user explicitly asks about Android OR iOS specifically.
    Args:
        query: the search query
        platform: either 'android' or 'ios'
    """
    results = vector_store.similarity_search(
        query,
        k=4,
        filter={"platform": platform.lower()}  # Chroma metadata filter
    )

    if not results:
        return f"No {platform} documentation found for that query."

    formatted = []
    for chunk in results:
        source = f"[{chunk.metadata['platform'].upper()} — {chunk.metadata['topic']}]"
        formatted.append(f"{source}\n{chunk.page_content}")

    return "\n\n---\n\n".join(formatted)


@tool
def get_code_example(topic: str, platform: str) -> str:
    """
    Returns a concise code example for a telemetry topic on Android or iOS.
    Use this when the user asks 'how do I implement', 'show me code',
    or 'give me an example' for a specific telemetry feature.
    Args:
        topic: the telemetry feature e.g. 'ANR detection', 'battery monitoring'
        platform: either 'android' or 'ios'
    """
    # We combine the topic with a code-focused query so Chroma
    # retrieves the most implementation-relevant chunks.
    code_query = f"{topic} implementation example code snippet {platform}"
    results = vector_store.similarity_search(code_query, k=3)

    if not results:
        return f"No code examples found for {topic} on {platform}."

    formatted = []
    for chunk in results:
        source = f"[{chunk.metadata['platform'].upper()} — {chunk.metadata['topic']}]"
        formatted.append(f"{source}\n{chunk.page_content}")

    return "\n\n---\n\n".join(formatted)
