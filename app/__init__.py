from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from flask.ext.bower import Bower

Bower(app)

from app import views
