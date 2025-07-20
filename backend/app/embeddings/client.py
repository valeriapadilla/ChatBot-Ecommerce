import logging
from dotenv import load_dotenv, find_dotenv
from langchain_openai import OpenAIEmbeddings
from app.config.settings import OPENAI_API_KEY

logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    openai_api_key=OPENAI_API_KEY
)

def embed_text(text: str) -> list[float]:
    try:
        logger.info("Generating embedding for text of length %d", len(text))
        embedding = embeddings.embed_query(text)
        logger.info("Embedding generated successfully, dimension: %d", len(embedding))
        return embedding
    except Exception as e:
        logger.error("Failed to generate embedding: %s", str(e))
        raise
