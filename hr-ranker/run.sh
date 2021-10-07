#!/bin/bash
# Run Script Application
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


exec gunicorn --workers="$WORKERS" --bind="$HOST:$PORT" --worker-class=uvicorn.workers.UvicornWorker \
--log-level="$LOG_LEVEL" --max-requests="$LIMIT_MAX_REQUEST" --keep-alive="$TIMEOUT_KEEP_ALIVE" application:app
