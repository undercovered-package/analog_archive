# Darkroom

Full-stack web application with a FastAPI backend, PostgreSQL database via Tortoise ORM, and a React frontend. Everything runs in Docker.

## Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Tortoise ORM (async) + asyncpg |
| Database | PostgreSQL 16 |
| Frontend | React 18 + TypeScript + Vite + TanStack Query + Tailwind CSS |
| Container | Docker + Docker Compose |
| Web server | Nginx (serves frontend + proxies API) |

## Project Structure

```
darkroom/
├── backend/
│   ├── app/
│   │   ├── config.py          # Settings + Tortoise ORM config
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── models/
│   │   │   └── item.py        # Item database model
│   │   └── routers/
│   │       ├── health.py      # GET /health
│   │       └── items.py       # CRUD /api/v1/items
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── api/client.ts      # Axios API client
│   │   ├── components/
│   │   │   ├── HealthCheck.tsx
│   │   │   └── Items.tsx
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
├── docker/
│   ├── backend/Dockerfile
│   ├── frontend/
│   │   ├── Dockerfile         # Multi-stage: Node build → Nginx
│   │   └── nginx.conf         # SPA routing + API proxy
│   ├── docker-compose.yml
│   └── .env.example           # Environment variable template
└── scripts/
    ├── start.sh               # Build and start all services
    └── stop.sh                # Stop all services
```

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

That's it — no local Node.js or Python required.

## Quick Start

```bash
# Clone the repo and enter the directory
git clone <repo-url>
cd darkroom

# Start everything (builds images on first run)
./scripts/start.sh
```

On first run the script copies `docker/.env.example` to `docker/.env` automatically.

| Service | URL |
|---|---|
| Frontend | http://localhost |
| Backend API | http://localhost:8000 |
| Swagger / OpenAPI docs | http://localhost:8000/docs |
| Health check | http://localhost:8000/health |

## Stop Services

```bash
./scripts/stop.sh
```

## Configuration

Environment variables live in `docker/.env` (created automatically from `docker/.env.example`):

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=darkroom
```

Edit this file before starting if you want to change database credentials. The backend `DATABASE_URL` is assembled from these values automatically by Docker Compose.

For local backend development (outside Docker), copy `backend/.env.example` to `backend/.env` and set `DATABASE_URL` to point to your local Postgres instance.

## API Endpoints

### Health

```
GET /health
```

Returns API and database status.

```json
{
  "status": "ok",
  "database": "healthy"
}
```

### Items

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/v1/items` | List all items |
| `POST` | `/api/v1/items` | Create an item |
| `GET` | `/api/v1/items/{id}` | Get item by ID |
| `DELETE` | `/api/v1/items/{id}` | Delete item by ID |

**Create item request body:**
```json
{
  "name": "My item",
  "description": "Optional description"
}
```

Full interactive docs available at http://localhost:8000/docs.

## Development (without Docker)

### Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and edit env
cp .env.example .env

# Run (requires a running Postgres instance)
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server (proxies /api and /health to localhost:8000)
npm run dev
```

Frontend dev server runs at http://localhost:3000.

## Rebuilding After Code Changes

```bash
./scripts/stop.sh
./scripts/start.sh
```

Or rebuild a single service:

```bash
docker compose -f docker/docker-compose.yml up -d --build backend
docker compose -f docker/docker-compose.yml up -d --build frontend
```

## Viewing Logs

```bash
# All services
docker compose -f docker/docker-compose.yml logs -f

# Single service
docker compose -f docker/docker-compose.yml logs -f backend
docker compose -f docker/docker-compose.yml logs -f frontend
docker compose -f docker/docker-compose.yml logs -f postgres
```

## Database

The database schema is created automatically on backend startup via Tortoise ORM (`generate_schemas=True`). No manual migration step is needed for a fresh start.

PostgreSQL data is persisted in a Docker volume (`postgres_data`). To reset the database completely:

```bash
docker compose -f docker/docker-compose.yml down -v
./scripts/start.sh
```
