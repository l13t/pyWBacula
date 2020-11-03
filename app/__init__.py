from flask import Flask, Blueprint
from app.reports.views import reports
from app.views import statics
import chartkick
import config

webapp = Flask(__name__)
webapp.config.from_object('config')

ck = Blueprint('ck_page', __name__, static_folder=chartkick.js(), static_url_path='/static')

webapp.register_blueprint(ck, url_prefix='/ck')
webapp.jinja_env.add_extension("chartkick.ext.charts")
webapp.jinja_env.add_extension('jinja2.ext.do')

# Adding routes
webapp.register_blueprint(statics)
webapp.register_blueprint(reports)
