from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from dotenv import load_dotenv
import os

load_dotenv()

# Where Chroma will save its data on disk.
# This folder gets created automatically.
CHROMA_PATH = "chroma_db"

def build_vector_store(docs: list[dict]) -> Chroma:
    """
    Chunks, embeds, and stores docs in Chroma.
    Safe to run multiple times — clears old data first.
    """
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    # If a DB already exists on disk, wipe it before re-ingesting.
    # This makes ingest_run.py safe to re-run whenever you add new docs.
    if os.path.exists(CHROMA_PATH):
        print(f"Existing Chroma DB found — clearing it before re-ingesting...")
        import shutil
        shutil.rmtree(CHROMA_PATH)

    documents = []
    for doc in docs:
        documents.append(Document(
            page_content=doc["text"],
            metadata={
                "platform": doc["platform"],
                "topic": doc["topic"],
                "url": doc["url"],
            }
        ))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " "],
    )
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks from {len(documents)} documents")

    print("Embedding and storing in Chroma (this may take ~30 seconds)...")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
    )

    print(f"✓ Stored {len(chunks)} chunks in Chroma at ./{CHROMA_PATH}")
    return vector_store


def load_vector_store() -> Chroma:
    """
    Loads an existing Chroma DB from disk.
    Use this after ingest is done — no re-embedding needed.
    """
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )
