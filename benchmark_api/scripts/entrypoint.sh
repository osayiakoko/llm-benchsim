#!/bin/sh

echo 'Running migrations...'
alembic upgrade head

echo 'Running server...'
exec uvicorn src.main:app --host 0.0.0.0 --port 8000 
