from app import config
from flask import Flask, Blueprint
import chartkick

app = Flask(__name__)
app.config.from_object('config')

db = create_engine(config.DB_URI, echo=True)

custom_path = config.CUSTOM_PATH

ck = Blueprint('ck_page', __name__, static_folder=chartkick.js(), static_url_path='/static')
app.register_blueprint(ck, url_prefix='/ck')
app.jinja_env.add_extension("chartkick.ext.charts")
app.jinja_env.add_extension('jinja2.ext.do')
