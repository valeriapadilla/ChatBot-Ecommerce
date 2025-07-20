import os
import logging
from pathlib import Path
from dotenv import load_dotenv
import psycopg2

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / '.env'
load_dotenv(env_path)

DB_HOST = os.getenv('POSTGRES_HOST')
DB_PORT = os.getenv('POSTGRES_PORT')
DB_NAME = os.getenv('POSTGRES_DB')
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')

def get_db_connection():
    try:
        logger.info("Connecting to database at %s:%s/%s", DB_HOST, DB_PORT, DB_NAME)
        connection = psycopg2.connect(
            host     = DB_HOST,
            port     = DB_PORT,
            dbname   = DB_NAME,
            user     = DB_USER,
            password = DB_PASSWORD
        )
        logger.info("Database connection established successfully")
        return connection
    except Exception as e:
        logger.error("Failed to connect to database: %s", str(e))
        raise
