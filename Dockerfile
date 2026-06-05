FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY docker/config.py config.py

RUN mkdir -p /tmp/custom_reports && chmod +x docker/entrypoint.sh

EXPOSE 15995

ENTRYPOINT ["docker/entrypoint.sh"]
CMD ["gunicorn", "-c", "docker/gunicorn.conf.py", "run:webapp"]
