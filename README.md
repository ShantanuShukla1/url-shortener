# Distributed URL Shortener

A distributed URL shortening service built with FastAPI and PostgreSQL, deployed on AWS EC2 with Route 53 for DNS routing and S3 for static asset storage. Uses a Redis caching layer to serve high-frequency redirects with sub-millisecond latency, reducing database load under high throughput. Containerized with Docker and configured with Nginx as a reverse proxy to distribute traffic and maintain fault tolerance across instances.

## Stack
- **FastAPI** — REST API layer
- **PostgreSQL** — persistent storage for URL mappings
- **Redis** — caching layer for high-frequency redirects
- **Nginx** — reverse proxy in front of the app
- **Docker / Docker Compose** — containerization and orchestration
- **AWS EC2** — deployment host
- **AWS Route 53** — DNS routing
- **AWS S3** — static asset storage

## Prerequisites
- Docker Desktop installed and running

## Running locally

1. Clone the repo:
2. Start all services:
3. Visit:
   - API: http://localhost:8000
   - Interactive docs (Swagger UI): http://localhost:8000/docs
   - Via Nginx reverse proxy: http://localhost

## Example usage

**Shorten a URL**

`POST /shorten`
```json
{ "original_url": "https://www.google.com" }
```

Response:
```json
{ "short_code": "aZ3xQ1", "original_url": "https://www.google.com" }
```

**Use the short URL**

Visit `http://localhost:8000/aZ3xQ1` — this redirects to the original URL. The first lookup hits Postgres and populates the Redis cache; subsequent lookups are served from Redis.

## Architecture
Client
│
▼
Nginx (reverse proxy)
│
▼
FastAPI app
│
├──▶ Redis (cache check first)
│
└──▶ PostgreSQL (source of truth, cache-miss fallback)
- **POST /shorten** — generates a unique short code, stores the mapping in Postgres
- **GET /{short_code}** — checks Redis first; on a cache miss, queries Postgres, increments the click count, then populates Redis for next time
- **GET /** — health check route

## Deployment

Deployed on an AWS EC2 instance running Docker Compose, with:
- **Route 53** mapping a custom domain to the EC2 instance's public IP
- **S3** serving static assets
- **Nginx** on the instance handling reverse proxy duties and distributing traffic across app containers

## Screenshots

## Local development notes
- `requirements.txt` — Python dependencies
- `Dockerfile` — builds the FastAPI app image
- `docker-compose.yml` — orchestrates app, Postgres, Redis, and Nginx together
- `nginx/nginx.conf` — reverse proxy configuration
