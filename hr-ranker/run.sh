#!/bin/bash
# Run Script Application
PYTHONPATH="${PYTHONPATH:-/app}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8080}"
LOG_LEVEL="${LOG_LEVEL:-info}"
WORKERS="${WORKERS:-2}"
LIMIT_MAX_REQUEST="${LIMIT_MAX_REQUEST:-20}"
TIMEOUT_KEEP_ALIVE="${TIMEOUT_KEEP_ALIVE:-10}"
LIMIT_MAX_CONCURRENCY="${LIMIT_MAX_CONCURRENCY:-10}"


echo "APPLICATION STARTING WITH PARAMS:"
echo "==========================="
echo "PYTHONPATH: [$PYTHONPATH]"
echo "HOST: [$HOST]"
echo "PORT: [$PORT]"
echo "LOG_LEVEL: [$LOG_LEVEL]"
echo "WORKERS: [$WORKERS]"
echo "LIMIT_MAX_REQUEST: [$LIMIT_MAX_REQUEST]"
echo "TIMEOUT_KEEP_ALIVE: [$TIMEOUT_KEEP_ALIVE]"
echo "LIMIT_MAX_CONCURRENCY: [$LIMIT_MAX_CONCURRENCY]"
echo "==========================="

echo "========Sarting application======="
gunicorn --workers="$WORKERS" --bind="$HOST:$PORT" --worker-class=uvicorn.workers.UvicornWorker \
--log-level="$LOG_LEVEL" --max-requests="$LIMIT_MAX_REQUEST" --keep-alive="$TIMEOUT_KEEP_ALIVE" application:app