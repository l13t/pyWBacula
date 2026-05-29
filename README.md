# pyWBacula

Web reports interface for [Bacula](https://www.bacula.org/) backup software.

Shows information not available in standard Bacula web UIs: big files in backups, long-running jobs, pool usage, per-job backup duration charts.

## Features

- **Reports**: jobs status, big files (per-server tabs, dynamic size filter), long-running backups, pool size, volume usage, backup duration chart
- **AJAX panel**: all reports load without full page reload
- **Charts**: Plotly-based size and file count charts per job
- **Health check**: `/health` endpoint
- **UI**: [Fomantic-UI 2.9.3](https://fomantic-ui.com/) + jQuery 3.7.1

## Requirements

- Python 3.8+
- PostgreSQL with Bacula catalog

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

## Docker image

```shell
docker pull ghcr.io/l13t/pywbacula:latest
```

Images are published to GitHub Container Registry on every release. Tags follow semver: `1.0.0`, `1.0`, `1`, `latest`.

## Releases

Versioning follows [Conventional Commits](https://www.conventionalcommits.org/):

- `fix:` → patch release
- `feat:` → minor release
- `feat!:` / `BREAKING CHANGE:` → major release
