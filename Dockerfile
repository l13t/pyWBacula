FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY docker/config.py config.py

RUN mkdir -p /tmp/custom_reports && chmod +x docker/entrypoint.sh

EXPOSE 15995

ENTRYPOINT ["docker/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:15995", "--workers", "4", "--timeout", "90", "run:webapp"]
