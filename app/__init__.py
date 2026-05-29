from flask import Flask
from app.reports.views import reports
from app.views import statics
from chartkick.flask import chartkick_blueprint
import config

import pandas as pd
import json
import plotly
import plotly.express as px

webapp = Flask(__name__)
webapp.config.from_object('config')

webapp.register_blueprint(chartkick_blueprint, url_prefix='/ck')
webapp.jinja_env.add_extension('jinja2.ext.do')

# Adding routes
webapp.register_blueprint(statics)
webapp.register_blueprint(reports)
