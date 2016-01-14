from flask import Flask, Blueprint

app = Flask(__name__)
app.config.from_object('config')

from flask.ext.bower import Bower
import pygal
import json
from urllib2 import urlopen
from pygal.style import DarkSolarizedStyle
#from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine

from app import config
db = create_engine(config.DB_URI, echo=True)

from app import views
import chartkick

ck = Blueprint('ck_page', __name__, static_folder=chartkick.js(), static_url_path='/static')
app.register_blueprint(ck, url_prefix='/ck')
app.jinja_env.add_extension("chartkick.ext.charts")
