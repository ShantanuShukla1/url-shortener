# Distributed URL Shortener

A distributed URL shortening service built with FastAPI and PostgreSQL, deployed on AWS EC2 with Route 53 for DNS routing. Uses a Redis caching layer to serve high-frequency redirects with sub-millisecond latency, reducing database load under high throughput. Containerized with Docker and configured with Nginx as a reverse proxy to serve the frontend, route API traffic, and maintain fault tolerance.

**Live demo:** [http://shortn.online](http://shortn.online)
**Live API docs (Swagger UI):** [http://shortn.online/docs](http://shortn.online/docs)

## Stack
- **FastAPI** — REST API layer
- **PostgreSQL** — persistent storage for URL mappings
- **Redis** — caching layer for high-frequency redirects
- **Nginx** — reverse proxy, also serves the static landing page
- **Docker / Docker Compose** — containerization and orchestration
- **AWS EC2** — deployment host, with an Elastic IP for a stable address
- **AWS Route 53** — DNS routing for the custom domain

## Prerequisites
- Docker Desktop installed and running

## Running locally

1. Clone the repo:
git clone https://github.com/ShantanuShukla1/url-shortener.git
cd url-shortener
2. Start all services:
docker-compose up --build
3. Visit:
   - Landing page (via Nginx): http://localhost
   - API root: http://localhost:8000
   - Interactive docs (Swagger UI): http://localhost:8000/docs

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

Visit `http://localhost:8000/aZ3xQ1` (or `http://shortn.online/aZ3xQ1` on the live version) — this redirects to the original URL. The first lookup hits Postgres and populates the Redis cache; subsequent lookups are served from Redis.

You can also use the landing page UI at `/` — paste a URL into the form and it calls `/shorten` for you, returning a clickable short link.

## Architecture
Client
│
▼
Nginx (reverse proxy)
│
├──▶ Static landing page (index.html) at "/"
│
└──▶ FastAPI app (all other routes)
│
├──▶ Redis (cache check first)
│
└──▶ PostgreSQL (source of truth, cache-miss fallback)
- **GET /** — serves the static landing page (via Nginx)
- **POST /shorten** — generates a unique short code, stores the mapping in Postgres
- **GET /{short_code}** — checks Redis first; on a cache miss, queries Postgres, increments the click count, then populates Redis for next time
- **GET /docs** — interactive Swagger UI

## Deployment

Deployed on an AWS EC2 instance (Ubuntu, t3.micro) running the full Docker Compose stack:

- **Elastic IP** attached to the instance so the public address stays fixed across restarts
- **Route 53** hosted zone mapping `shortn.online` to the Elastic IP via an A record
- **Nginx** on the instance serves the landing page and reverse-proxies everything else to the FastAPI container
- **Postgres healthcheck** in `docker-compose.yml` ensures the app container waits for the database to be ready before starting, and `restart: unless-stopped` lets it recover automatically if it ever crashes

To deploy updates to the live instance:
```bash
ssh -i <your-key>.pem ubuntu@<elastic-ip>
cd url-shortener
git pull
docker compose down
docker compose up --build -d
```

## Screenshots

<img width="2549" height="1293" alt="urlshortenerfrontend" src="https://github.com/user-attachments/assets/64c6c4cf-a579-4602-86de-812e9201c2c2" />
<img width="841" height="486" alt="shortlinkgeneration" src="https://github.com/user-attachments/assets/ae532811-81d7-43f0-a2b4-01f2c4bef3e1" />
<img width="2525" height="1279" alt="swaggerui" src="https://github.com/user-attachments/assets/7afce750-dcb0-4fad-81cd-4a414223ce85" />
<img width="1954" height="428" alt="urlshorteneroncloud" src="https://github.com/user-attachments/assets/4cd913d2-e631-4d10-95b0-c3b45a5b3d3c" />
<img width="2131" height="285" alt="ec2instance" src="https://github.com/user-attachments/assets/c0b06901-6902-435e-a039-afc5460f0c6c" />
<img width="2079" height="362" alt="hostedzone" src="https://github.com/user-attachments/assets/9108a97e-cd5a-4c4b-86b7-f107d52f60e2" />
<img width="509" height="668" alt="folderstructure" src="https://github.com/user-attachments/assets/79032107-0f11-450e-9bb2-e61940e00ebb" />

## Project files
- `app/` — FastAPI application code (routes, models, database, cache)
- `nginx/nginx.conf` — reverse proxy + static file serving config
- `nginx/index.html` — static landing page UI
- `requirements.txt` — Python dependencies
- `Dockerfile` — builds the FastAPI app image
- `docker-compose.yml` — orchestrates app, Postgres, Redis, and Nginx together
