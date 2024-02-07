#!/bin/sh
# run_dev.sh
litestream replicate -config litestream.yml

alembic upgrade head

uvicorn src.api.main:app --reload --workers 1 --host 0.0.0.0