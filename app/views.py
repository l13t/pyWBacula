#### Import section ####
from flask import render_template, request, send_from_directory, Flask, jsonify
from app import app
from app import db
from sqlalchemy import desc, asc
from sqlalchemy.sql import and_, or_, not_, select, func
import os
from datetime import time, datetime, date, timedelta
from time import gmtime, strftime
from database import *
from lib import *
#### End of import section ####

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

@app.route('/favicon.ico')
def favicon():
  return send_from_directory(os.path.join(app.root_path, 'static/img'), 'bacula.png', mimetype='image/png')

@app.route('/')
@app.route('/home')
def index():
  s = select([jobhist.c.name, jobhist.c.schedtime, jobhist.c.jobbytes], use_labels=True).where(jobhist.c.schedtime > (date.today() - timedelta(days=28)))
  result = db.execute(s).fetchall()
  b_s_result = gen_chart_array_time_3d(result)
  s = select([jobhist.c.name, jobhist.c.schedtime, jobhist.c.jobfiles], use_labels=True).where(jobhist.c.schedtime > (date.today() - timedelta(days=28)))
  result = db.execute(s).fetchall()
  b_c_result = gen_chart_array_time_3d(result)
  s = select([client.c.name, job.c.name, job.c.schedtime, job.c.jobfiles, job.c.jobbytes],  use_labels=True).where(and_(job.c.schedtime > (datetime.now() - timedelta(hours=24)), client.c.clientid == job.c.clientid)).order_by(job.c.name)
  result = db.execute(s).fetchall()
  detailed_result_last_day = [{'name': str(k)+" ("+str(x)+")", 'date': y.strftime('%Y-%m-%d'), 'files': int(z), 'size': sizeof_fmt(int(i))} for k, x, y, z, i in result]
  return render_template("index.html", title='Home page', b_size=b_s_result, b_count=b_c_result, last_backup=detailed_result_last_day)

@app.route('/login')
def login():
  return render_template("login.html", title='Login to statistics page')

@app.route('/api/login', methods=['POST'])
def check_login():
  login=request.form["login"]
  pwd=request.form["pwd"]
  return "Hello, %s !" % auth.username()

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html', title="Page not found"), 404

@app.route('/reports')
def reports():
  return render_template('reports.html', title='Available reports list')

@app.route('/reports/jobs', methods=['POST'])
def jobs_report():
  s = select([job,client], use_labels=True).where(job.c.clientid == client.c.clientid).where(or_(client.c.name.like('jotun%'), client.c.name.like('%heimr%'))).order_by(job.c.jobid.desc())
  #s = select([(client.c.name)]).where(client.c.name.like('jotun%'))
  
  result = db.execute(s).fetchall()

  return render_template('jobs_report.html', title='Jobs report', jobs = result)

@app.route('/reports/big_files', methods=['POST'])
def big_files_report():
  s = select([job.c.name]).where(job.c.starttime > datetime.now() - timedelta(hours=24))
  result = db.execute(s).fetchall()
  proceed_result = {}
  for res in result:
    job_i = str(res[0])
    s = select([path.c.path, filename.c.name, files.c.lstat]).where(
        and_(
            job.c.name == job_i,
            job.c.jobid == files.c.jobid,
            job.c.starttime > datetime.now() - timedelta(hours=24),
            filename.c.filenameid == files.c.filenameid,
            path.c.pathid == files.c.pathid
            )
        )
    out_res = db.execute(s)
    proceed_result[job_i] = show_decoded_big_files_results(out_res, 10)
  return render_template('bigfiles_report.html', title='Big files report', bf_report=proceed_result, res=result)

@app.route('/reports/pool_size_report', methods=['POST'])
def pool_size_report():
  s = select([pool.c.name, job.c.schedtime, func.sum(job.c.jobbytes).label("pool_size")], use_labels=True).where(
      and_(
          job.c.schedtime > (date.today() - timedelta(days=28)),
          job.c.poolid == pool.c.poolid
          )
      ).group_by(pool.c.name, job.c.schedtime)
  result = db.execute(s).fetchall()
  p_s_result = gen_chart_array_time_3d(result)
  s = select(
    [storage.c.name, jobhist.c.schedtime, func.sum(jobhist.c.jobbytes).label("storage_size")]
  ).where(
    and_(
      jobhist.c.jobid == jobmedia.c.jobid,
      storage.c.storageid == media.c.storageid,
      jobmedia.c.mediaid == media.c.mediaid,
      jobhist.c.schedtime > (date.today() - timedelta(days=28)),
    )
  ).group_by(storage.c.name, jobhist.c.schedtime)
  result = db.execute(s).fetchall()
  s_s_result = gen_chart_array_time_3d(result)
  return render_template("pool_size.html", title='Pool size report', p_size=p_s_result, s_size = s_s_result, res=result)
