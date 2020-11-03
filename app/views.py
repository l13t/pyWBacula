from datetime import datetime, date, timedelta
from flask import Blueprint, render_template, request, redirect, send_from_directory
from sqlalchemy import cast, Date
from sqlalchemy.sql import and_, select, func
from time import gmtime, strptime, mktime
from libs import pwb, static_vars
from app.db import db
from bokeh.plotting import figure, output_file, show, curdoc
import config
import gviz_api
import os
import re

statics = Blueprint('statics', __name__)

custom_path = config.CUSTOM_PATH

@statics.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(statics.root_path, 'static/img'), 'bacula.png', mimetype='image/png')


@statics.route('/', methods=['GET'])
@statics.route('/home', methods=['GET', 'POST'])
def index():
    if re.match("Wget", request.headers.get('User-Agent')):
        return render_template("ok_mon_server.html", title="Home page")
    # s1 = select([client.c.name, job.c.name, job.c.jobstatus, job.c.schedtime, job.c.jobfiles, job.c.jobbytes],
    # use_labels=True).where(and_(client.c.clientid == job.c.clientid,
    # jobhist.c.schedtime > date.today() - timedelta(days=56)))

    # s2 = select([client.c.name, jobhist.c.name.label('job_name'), jobhist.c.jobstatus, jobhist.c.schedtime,
    # jobhist.c.jobfiles, jobhist.c.jobbytes],  use_labels=True).where(and_(client.c.clientid == jobhist.c.clientid,
    # jobhist.c.schedtime > date.today() - timedelta(days=56)))
    # query = s1.union(s2).alias('job_name')
    query = """
    SELECT client.name AS client_name, job.name AS job_name, job.jobstatus AS job_jobstatus,
        job.schedtime AS job_schedtime, job.jobfiles AS job_jobfiles, job.jobbytes AS job_jobbytes
    FROM
        client, job
    WHERE
        client.clientid = job.clientid AND job.schedtime > now() - interval '28 days'
    UNION
        SELECT client.name AS client_name, jobhisto.name AS job_name,
            jobhisto.jobstatus AS jobhisto_jobstatus, jobhisto.schedtime AS
            jobhisto_schedtime, jobhisto.jobfiles AS jobhisto_jobfiles, jobhisto.jobbytes AS jobhisto_jobbytes
        FROM
            client, jobhisto
        WHERE
            client.clientid = jobhisto.clientid AND jobhisto.schedtime > now() - interval '28 days';
    """
    result = db.execute(query).fetchall()
    b_s_res = []
    b_c_res = []
    detailed_result_last_day = []
    for j, tmp in enumerate(result):
        k, x, st, y, z, i = tmp
        b_s_res.append((k, y, i))
        b_c_res.append((k, y, z))
        if y > datetime.now() - timedelta(hours=24):
            detailed_result_last_day.append({'name': str(k),
                                             'bak_name': str(x),
                                             'date': y.strftime('%Y-%m-%d %H:%M:%S'),
                                             'files': int(z),
                                             'size': pwb.sizeof_fmt(int(i)),
                                             'status': static_vars.JobStatus[st]})
    b_s_result = pwb.gen_chart_array_time_3d(b_s_res)
    b_c_result = pwb.gen_chart_array_time_3d(b_c_res)

    b_s_result_plot = figure(name="b_s_result")
    for item in b_s_result:
        y, x = zip(*item['data'].items())
        b_s_result_plot.line(x, y, legend_label=item['name'])
    curdoc().add_root(b_s_result_plot)

    return render_template("index.html",
                           title='Home page',
                           b_size=b_s_result,
                           b_count=b_c_result,
                           last_backup=detailed_result_last_day,
                           tmp=result)


@statics.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title="Page not found"), 404


@statics.route('/about', methods=['GET'])
def about_page():
    return render_template('about.html', title="About page")

@statics.route('/health', methods=['GET'])
def pwb_health():
    return render_template("ok_mon_server.html", title="Home page")