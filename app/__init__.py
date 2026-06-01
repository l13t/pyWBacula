from flask import Flask
from app.reports.views import reports
from app.views import statics
import config

webapp = Flask(__name__)
webapp.config.from_object('config')

webapp.jinja_env.add_extension('jinja2.ext.do')

# Adding routes
webapp.register_blueprint(statics)
webapp.register_blueprint(reports)
