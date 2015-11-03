from flask import render_template
from app import app

@app.route('/')
@app.route('/home')
def index():
  return render_template("index.html", title='Home page')

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404
