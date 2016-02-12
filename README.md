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
