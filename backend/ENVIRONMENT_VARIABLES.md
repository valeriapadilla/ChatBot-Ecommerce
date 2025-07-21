# Environment Variables

This document describes all environment variables for the RAG Chat API.

## Required Variables

### OpenAI Configuration
- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Database Configuration
- `POSTGRES_HOST`: PostgreSQL host
- `POSTGRES_PORT`: PostgreSQL port
- `POSTGRES_USER`: PostgreSQL username
- `POSTGRES_PASSWORD`: PostgreSQL password
- `POSTGRES_DB`: PostgreSQL database name

### JWT Configuration
- `JWT_SECRET_KEY`: Secret key for signing JWT tokens (required, use a long random string)
- `JWT_ALGORITHM`: Algorithm for JWT (default: HS256)
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration in minutes (default: 1440)

## Optional Variables (with defaults)

### Server Configuration
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `RELOAD`: Enable auto-reload (default: true)
- `LOG_LEVEL`: Logging level (default: info)

### Application Configuration
- `APP_NAME`: Application name (default: RAG Chat API)
- `APP_VERSION`: Application version (default: 1.0.0)
- `APP_DESCRIPTION`: Application description

### CORS Configuration
- `CORS_ORIGINS`: Allowed origins (default: ["*"])
- `CORS_CREDENTIALS`: Allow credentials (default: true)
- `CORS_METHODS`: Allowed methods (default: ["*"])
- `CORS_HEADERS`: Allowed headers (default: ["*"])

### API Configuration
- `API_PREFIX`: API prefix (default: /api/v1)
- `DOCS_URL`: Documentation URL (default: /docs)
- `REDOC_URL`: ReDoc URL (default: /redoc)

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure
- Use strong passwords for database connections
- User passwords are hashed using bcrypt
- Session IDs should be unique per user session

