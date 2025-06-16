#!/bin/bash
set -e

echo "Initializing database if needed..."
python scripts/init_postgres.py

echo "Running Alembic migrations..."
alembic upgrade head

echo "Backend bootstrap complete."
