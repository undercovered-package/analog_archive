#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Copy .env if it doesn't exist yet
if [ ! -f "$ROOT/docker/.env" ]; then
  cp "$ROOT/docker/.env.example" "$ROOT/docker/.env"
  echo "Created docker/.env from example — edit it to change credentials."
fi

echo "Building and starting services..."
docker compose -f "$ROOT/docker/docker-compose.yml" up -d --build

echo ""
echo "Services running:"
echo "  Frontend  → http://localhost"
echo "  Backend   → http://localhost:8000"
echo "  API docs  → http://localhost:8000/docs"
echo "  Health    → http://localhost:8000/health"
