FROM python:3.11-slim as main

LABEL description="Intime Biotech: Backend" \
      version="1.0.0" \
      maintainer="https://github.com/DPavlen/"

ENV SRC_DIR=/app \
    APP_USER=backend-user \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GUNICORN_PROCESSES=4 \
    GUNICORN_CONNECTIONS=8 \
    GUNICORN_LOGLEVEL='error'

RUN apt-get update && \
    apt-get install -y dos2unix

ENV PATH="/$SRC_DIR/.local/bin:${PATH}"

RUN pip install --upgrade pip && \
    pip install --no-cache-dir poetry

COPY pyproject.toml pyproject.toml
RUN poetry install --no-root --only main

COPY ./backend /$SRC_DIR
COPY docker/backend/entrypoint.sh /usr/local/bin/entrypoint.sh

EXPOSE 8000

RUN chmod +x /$SRC_DIR/run_django.sh && \
    dos2unix /$SRC_DIR/run_django.sh

CMD ["bash", "/app/run_django.sh"]

FROM main as test

COPY ./backend /app

RUN poetry run python /app/manage.py makemigrations
RUN poetry run python /app/manage.py migrate

RUN poetry install --no-root
