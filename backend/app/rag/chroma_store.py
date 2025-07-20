import logging
from pathlib import Path
from dotenv import load_dotenv
from langchain_chroma import Chroma
from app.embeddings.client import embeddings

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT / ".env")

vectorstore = Chroma(
    persist_directory=str(ROOT / "data" / "chroma"),
    embedding_function=embeddings
)

def add_documents(docs: list[dict]) -> None:
    try:
        logger.info("Adding %d documents to vector store", len(docs))
        texts = [d["text"] for d in docs]
        metadatas = [d.get("metadata", {}) for d in docs]

        vectorstore.add_texts(
            texts=texts,
            metadatas=metadatas
        )
        logger.info("Successfully added %d documents to vector store", len(docs))
    except Exception as e:
        logger.error("Failed to add documents to vector store: %s", str(e))
        raise