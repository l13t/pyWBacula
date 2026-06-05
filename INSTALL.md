# Installation

## Quick start with Docker

```shell
git clone https://github.com/l13t/pyWBacula.git
cd pyWBacula
cp config.py.example config.py   # edit DB_URI if needed
docker compose up --build
```

App available at `http://localhost:15995`

## Manual installation

```shell
git clone https://github.com/l13t/pyWBacula.git
cd pyWBacula
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### Configuration

Set environment variables or edit `config.py`:

| Variable | Example | Description |
|----------|---------|-------------|
| `DB_URI` | `postgresql://bacula:bacula@localhost/bacula?client_encoding=utf8` | PostgreSQL connection string |
| `SECRET_KEY` | `change-me` | Flask secret key |
| `CUSTOM_PATH` | `/tmp/custom_reports/` | Path for custom report scripts |
| `PWB_HOST` | `0.0.0.0` | Bind address |

### Run

```shell
python run.py
# or
gunicorn --bind 0.0.0.0:15995 run:webapp
```
