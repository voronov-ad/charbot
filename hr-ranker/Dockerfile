FROM python:3.8.12-slim-buster
LABEL author='Voronov.A.Dm@sberbank.ru'
USER root
ARG token
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    APP_NAME=hr-ranker \
    BACKLOG=2048 \
    WORKERS=1 \
    LIMIT_MAX_REQUEST=100 \
    LIMIT_MAX_CONCURRENCY=10 \
    TIMEOUT_KEEP_ALIVE=5 \
    HOST=0.0.0.0 \
    SSL_REQ=2 \
    PORT=8001

EXPOSE ${PORT}
RUN mkdir -p /app
COPY ./* /app/

WORKDIR /app
RUN pip install -r ./requirements.txt
CMD sh run.sh