import json
import logging
import sys

from flask import Flask
from app.reports.views import reports
from app.views import statics
import config


class _JsonFormatter(logging.Formatter):
    def format(self, record):
        d = {
            'ts': self.formatTime(record, '%Y-%m-%dT%H:%M:%S'),
            'level': record.levelname,
            'logger': record.name,
            'msg': record.getMessage(),
        }
        if record.exc_info:
            d['exc'] = self.formatException(record.exc_info)
        return json.dumps(d)


def _setup_logging(debug: bool) -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(_JsonFormatter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(logging.DEBUG if debug else logging.INFO)
    logging.getLogger('sqlalchemy.engine').setLevel(
        logging.INFO if debug else logging.WARNING)
    logging.getLogger('sqlalchemy.pool').setLevel(logging.WARNING)


_debug = getattr(config, 'DEBUG', False)
_setup_logging(_debug)

webapp = Flask(__name__)
webapp.config.from_object('config')

webapp.jinja_env.add_extension('jinja2.ext.do')

webapp.register_blueprint(statics)
webapp.register_blueprint(reports)
