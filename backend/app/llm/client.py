import os
import logging
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from app.config.settings import OPENAI_API_KEY

logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    openai_api_key=OPENAI_API_KEY
)

def generate_chat_completion(messages: list[dict]) -> str:
    try:
        logger.info("Generating chat completion with %d messages", len(messages))
        response = llm.invoke(messages)
        logger.info("Chat completion generated successfully")
        return response.content
    except Exception as e:
        logger.error("Error generating chat completion: %s", str(e))
        raise
 