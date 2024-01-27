#!/bin/sh
# run_dev.sh
while ! nc -z db 5432; do
    echo "waiting for postgress listening..."
    sleep 0.1
done
echo "PostgreSQL started"

alembic upgrade head

uvicorn src.api.main:app --reload --workers 1 --host 0.0.0.0