# Makers Tech ChatBot

## Project Overview

Makers Tech ChatBot is an AI-powered assistant for ecommerce, capable of answering user questions about product inventory, features, and prices in real time through a conversational web interface. The solution leverages modern backend, frontend, and AI technologies to deliver a seamless and intelligent customer experience.

---

## Architecture & Technology Stack

**Backend:**
- **Python** with **FastAPI**: For building robust, high-performance REST APIs.
- **PostgreSQL**: As the relational database for storing product and user data.
- **RAG (Retrieval-Augmented Generation)**: Combines language models with real-time vector search for accurate, context-aware responses.
- **Chroma/Vector Store**: Stores product embeddings for semantic search.
- **Docker**: Containerizes backend and database for easy deployment.

**Frontend:**
- **React** with **Next.js**: For a modern, fast, and SEO-friendly user interface.
- **Tailwind CSS**: For rapid, responsive, and clean UI styling.
- **Docker**: Containerizes the frontend for consistent deployment.

**Orchestration:**
- **Docker Compose**: Manages multi-container setup (database, backend, frontend).

---

## Project Structure

```
chatBot/
  backend/
    app/           # FastAPI app, business logic, models, services
    db/            # Database init scripts, connection
    rag/           # RAG logic, vector store, seed script
    requirements.txt
    Dockerfile
  frontend/
    src/           # Next.js/React app
    Dockerfile
  docker-compose.yml
  README.md
```

---

## How to Run the Project

### 1. Clone the Repository

```bash
git clone <repo-url>
cd chatBot
```

### 2. Start Database with Docker Compose

This will start the PostgreSQL database in a Docker container.

```bash
docker-compose up -d db
```

Wait a few seconds for the database to initialize.

### 3. Seed the Vector Store

Before running the backend, you need to populate the vector store with product embeddings. This step reads products from the database and creates their semantic representations for AI-powered search.

```bash
# In a new terminal, enter the backend container:
docker-compose run --rm backend bash

# Inside the container, run the seed script:
python app/rag/seed_vector_db.py

# Exit the container
exit
```

### 4. Start Backend and Frontend

Now you can start the backend and frontend services:

```bash
docker-compose up -d backend frontend
```

- The **backend** (FastAPI) will be available at: [http://localhost:8000](http://localhost:8000)
- The **frontend** (Next.js) will be available at: [http://localhost:3000](http://localhost:3000)

---

## How It Works

- **User** interacts with the chatbot via the web interface (frontend).
- **Frontend** sends user questions to the backend API.
- **Backend** processes the question, retrieves product data from PostgreSQL, and uses RAG (embeddings + vector search) to find the most relevant information.
- **AI Model** generates a conversational, context-aware response.
- **Frontend** displays the answer to the user in real time.

---

## Useful Commands

- Stop all services:
  ```bash
  docker-compose down
  ```
- View logs:
  ```bash
  docker-compose logs -f backend frontend db
  ```
- Run backend tests:
  ```bash
  docker-compose run --rm backend pytest app/tests
  ```

---

## Notes
- Ensure your `.env` files are properly configured for database and API secrets.
- The seed script (`seed_vector_db.py`) must be run after the database is up and seeded with products.
- The backend and frontend can be developed locally or inside Docker containers as needed.

---
