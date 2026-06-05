# pyWBacula

Web reports interface for [Bacula](https://www.bacula.org/) backup software.

Shows information not available in standard Bacula web UIs: big files in backups, long-running jobs, pool usage, per-job backup duration charts.

## Features

- **Reports**: jobs status, big files (per-server tabs, dynamic size filter), long-running backups, pool size, volume usage, backup duration chart
- **AJAX panel**: all reports load without full page reload
- **Charts**: Plotly-based size and file count charts per job
- **Health endpoints**: `/health` (liveness), `/ready` (readiness — checks DB)
- **UI**: [Fomantic-UI 2.9.3](https://fomantic-ui.com/) + jQuery 3.7.1

## Requirements

- Python 3.8+
- PostgreSQL with Bacula catalog

→ See [INSTALL.md](INSTALL.md) for installation and configuration.

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
