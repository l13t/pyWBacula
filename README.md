# pyWBacula v0.1
Another one simple bacula web reports interface.

I wasn't satisfied with current web interfaces for bacula. Cause they show default information which I can get from console and doesn't show really useful information (like big files in backup, long-running-backups etc).

So as a result I start writing own web reports interface.

#Requirements
* Enabled bacula history for jobs
* PostgreSQL database (I use postgres on all my servers with bacula)
* python Flask

#Documentation
[Instalation notes](https://github.com/l13t/pyWBacula/wiki/Installation)

#Notes
* requirements.txt contains modules which I use in my web interface
* css is based on SemanticUI (http://semantic-ui.com/)
* for database connection I use SQLAlchemy

# Installation

## Download

`git clone https://github.com/l13t/pyWBacula.git`

## Prepare and enable virtual enviroment

```
cd pyWBacula
virtualenv venv
source venv/bin/activate
```

## Install python modules

`pip install -r requirements.txt`

## Modify configuration files

After downloading you should rename next configuration files:

`cp config.py.example config.py
cp app/config.py.example app/config.py`

### app/config.py syntax

* DB_URI:

`DB_URI = 'postgresql://<user>:<password>@<host>:<port>/<db_name>?client_encoding=utf8'`

> Currently only PostgreSQL supported.

# Run application

## Run in standalone mode

You can use _run.py_ to start application:

`./run.py`

Or you can use gunicorn:

`venv/bin/gunicorn --bind 0.0.0.0:15995 run:app`

## Run on startup

To run on startup just do next steps:

```
cp utils/pywbacula /etc/init.d/
chmod 755 /etc/init.d/pywbacula && chown root:root /etc/init.d/pywbacula
update-rc.d pywbacula defaults
update-rc.d pywbacula enable
```

Edit /etc/init.d/pywbacula to change WWW\_HOME and APP\_USER variables.

## Grafana+InfluxDB reports

In utils you can find scripts which would help you create graph reports with Grafana+InfluxDB.

* utils/bacula\_to\_influx - custom cronjob to push data to InfluxDB
* utils/results\_to\_influx.sh - script which push data to InfluxDB
* utils/grafana\_panel\_template.json - dashboard template for Grafana to show results

[![Updates](https://pyup.io/repos/github/l13t/pywbacula/shield.svg)](https://pyup.io/repos/github/l13t/pywbacula/)[![Python 3](https://pyup.io/repos/github/l13t/pywbacula/python-3-shield.svg)](https://pyup.io/repos/github/l13t/pywbacula/)
