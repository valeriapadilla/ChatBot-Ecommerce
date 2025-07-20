import logging
from db.connection import get_db_connection
from app.rag.chroma_store import add_documents

logger = logging.getLogger(__name__)

def extract_products():
    conn = get_db_connection()
    cur  = conn.cursor()
    cur.execute(
        "SELECT id, name, brand, features, price, quantity FROM products;"
        )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    logger.info("Found %d products in database", len(rows))
    
    if len(rows) == 0:
        logger.warning("No products found in database. Please run the database seed first.")
        return []

    docs = []
    for prod_id, name, brand, features, price, quantity in rows:
        text = f"{name} {brand} {features}"
        docs.append({
            "id": str(prod_id),
            "text": text,
            "metadata": {
                "price": float(price),
                "quantity": int(quantity)
            }
        })
    return docs

def seed_vector_db():
    logger.info("Starting vector store seed process")
    docs = extract_products()
    
    if len(docs) == 0:
        logger.error("No documents to add. Exiting.")
        return
        
    add_documents(docs)
    logger.info("Vector store seed completed successfully: inserted %d embeddings", len(docs))


if __name__ == "__main__":
    seed_vector_db()
