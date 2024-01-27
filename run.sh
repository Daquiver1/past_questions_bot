#!/bin/sh

alembic upgrade head

gunicorn -w 1 -k uvicorn.workers.UvicornWorker src.api.main:app --bind 0.0.0.0:8080