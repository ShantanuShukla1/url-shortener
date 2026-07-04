# Distributed URL Shortener

A distributed URL shortening service built with FastAPI and PostgreSQL, with a Redis caching layer for high-frequency redirects and Nginx as a reverse proxy.

## Stack
- FastAPI
- PostgreSQL
- Redis
- Docker / Docker Compose
- Nginx

## Running locally
1. Make sure Docker Desktop is running
2. `docker-compose up --build`
3. API available at `http://localhost:8000` (direct) or `http://localhost` (via Nginx)