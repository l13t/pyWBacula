#### Import section ####
from flask import render_template, request, redirect, send_from_directory, Flask, jsonify
from app import *
#from app import db
from sqlalchemy import desc, asc, cast, Date
from sqlalchemy.sql import and_, or_, not_, select, func
import os
from datetime import time, datetime, date, timedelta
from time import gmtime, strftime, strptime, mktime
from database import *
from lib import *
import static_vars
import re
#### End of import section ####

@app.route('/favicon.ico')
def favicon():
  return send_from_directory(os.path.join(app.root_path, 'static/img'), 'bacula.png', mimetype='image/png')

@app.route('/')
@app.route('/home')
def index():
  if re.match("Wget", request.headers.get('User-Agent')):
    return render_template("ok_mon_server.html", title="Home page")
  #s1 = select([client.c.name, job.c.name, job.c.jobstatus, job.c.schedtime, job.c.jobfiles, job.c.jobbytes],  use_labels=True).where(and_(client.c.clientid == job.c.clientid, jobhist.c.schedtime > date.today() - timedelta(days=56)))
  #s2 = select([client.c.name, jobhist.c.name.label('job_name'), jobhist.c.jobstatus, jobhist.c.schedtime, jobhist.c.jobfiles, jobhist.c.jobbytes],  use_labels=True).where(and_(client.c.clientid == jobhist.c.clientid, jobhist.c.schedtime > date.today() - timedelta(days=56)))
  #query = s1.union(s2).alias('job_name')
  query = """
  SELECT client.name AS client_name, job.name AS job_name, job.jobstatus AS job_jobstatus, job.schedtime AS job_schedtime, job.jobfiles AS job_jobfiles, job.jobbytes AS job_jobbytes
  FROM client, job
  WHERE client.clientid = job.clientid AND job.schedtime > now() - interval '28 days'
  UNION
  SELECT client.name AS client_name, jobhisto.name AS job_name, jobhisto.jobstatus AS jobhisto_jobstatus, jobhisto.schedtime AS
  jobhisto_schedtime, jobhisto.jobfiles AS jobhisto_jobfiles, jobhisto.jobbytes AS jobhisto_jobbytes
  FROM client, jobhisto
  WHERE client.clientid = jobhisto.clientid AND jobhisto.schedtime > now() - interval '28 days';
  """
  result = db.execute(query).fetchall()
  b_s_res = []
  b_c_res = []
  detailed_result_last_day = []
  for j, tmp in enumerate(result):
    k,x,st,y,z,i = tmp
    b_s_res.append( (k, y, i) )
    b_c_res.append( (k, y, z) )
    if y > datetime.now() - timedelta(hours=24):
      detailed_result_last_day.append({'name': str(k), 'bak_name': str(x), 'date': y.strftime('%Y-%m-%d %H:%M:%S'), 'files': int(z), 'size': sizeof_fmt(int(i)), 'status': static_vars.JobStatus[st]})
  b_s_result = gen_chart_array_time_3d(b_s_res)
  b_c_result = gen_chart_array_time_3d(b_c_res)
  return render_template("index.html", title='Home page', b_size=b_s_result, b_count=b_c_result, last_backup=detailed_result_last_day, tmp=result)

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html', title="Page not found"), 404

@app.route('/about')
def about_page():
  return render_template('about.html', title="About page")

@app.route('/contact_us')
def contacts_page():
  return render_template('contacts.html', title="Contact us")

@app.route('/reports')
def reports():
  unix_today = int(mktime(gmtime()))
  return render_template('reports.html', title='Available reports list', unix_date=unix_today)

@app.route('/reports/jobs', methods=['POST'])
def jobs_report():
  s = "SELECT client.name AS client_name, job.name AS job_name, job.jobstatus AS job_jobstatus, job.starttime AS job_startime, job.endtime AS job_endtime, job.schedtime AS job_schedtime, job.jobfiles AS job_jobfiles, job.jobbytes AS job_jobbytes, job.level as job_level FROM client, job, (select max(job.schedtime) as max_schedtime, job.name AS job_name from job group by job.name) as lj where lj.job_name = job.name and job.schedtime = lj.max_schedtime and client.clientid = job.clientid"
  query_result = db.execute(s).fetchall()
  result = []
  for i, res in enumerate(query_result):
    cname = res[0]
    jname = res[1]
    jstatus = res[2]
    jstart = res[3]
    jend = res[4]
    jsched = res[5]
    jdur = jend - jstart
    jstdur = jstart - jsched
    jfiles = res[6]
    jbytes = res[7]
    jlevel = res[8]
    if jsched > datetime.now() - timedelta(hours=24):
      old_job = False
    else:
      old_job = True
    result.append({
        'cname': cname,
        'jname': jname,
        'jstatus': static_vars.JobStatus[jstatus],
        'jstart': jstart.strftime('%Y-%m-%d %H:%M:%S'),
        'jend': jend.strftime('%Y-%m-%d %H:%M:%S'),
        'jsched': jsched,
        'jdur': jdur,
        'jstdur': jstdur,
        'jfiles': int(jfiles),
        'jbytes': sizeof_fmt(int(jbytes)),
        'jlevel': static_vars.JobLevel[jlevel],
        'old_job': old_job,
      })
  return render_template('jobs_report.html', title='Jobs report', jobs = result)

@app.route('/reports/big_files', methods=['GET', 'POST'])
def big_files_report():
  _max_size = 10
  if request.method == 'POST':
    _max_size = int(request.form['_max_size'])
  s = select([job.c.name, job.c.schedtime]).where(job.c.schedtime > datetime.now() - timedelta(hours=24))
  result = db.execute(s).fetchall()
  proceed_result = {}
  sched_time = {}
  for res in result:
    job_i = str(res[0])
    s = select([path.c.path, filename.c.name, files.c.lstat]).where(
        and_(
            job.c.name == job_i,
            job.c.jobid == files.c.jobid,
            job.c.schedtime > datetime.now() - timedelta(hours=24),
            filename.c.filenameid == files.c.filenameid,
            path.c.pathid == files.c.pathid
            )
        )
    out_res = db.execute(s)
    proceed_result[job_i] = show_decoded_big_files_results(out_res, 10)
    sched_time[job_i] = res[1].strftime("%Y-%m-%d %H:%M:%S")
  return render_template('bigfiles_report.html', title='Big files report', bf_report=proceed_result, res=result, sched_time=sched_time)

@app.route('/reports/pool_size_report', methods=['POST'])
def pool_size_report():
  s = """
  select
  pool.name as pool_name, job.schedtime as job_schedtime, sum(job.jobbytes) as pool_size
  from
  pool, job
  where
  job.schedtime > now() - interval '28 days' and job.poolid = pool.poolid
  group by
  pool.name, job.schedtime
  union
  select
  pool.name as pool_name, jobhisto.schedtime as job_schedtime, sum(jobhisto.jobbytes) as pool_size
  from
  pool, jobhisto
  where
  jobhisto.schedtime > now() - interval '28 days' and jobhisto.poolid = pool.poolid
  group by
  pool.name, jobhisto.schedtime
  order by
  job_schedtime, pool_name
  """
  result = db.execute(s).fetchall()
  s_s_result = gen_chart_array_time_3d(result)
  return render_template("pool_size.html", title='Pool size report', s_size = s_s_result)

@app.route('/reports/client/<host_name>/<bdate>')
def client_detailed_info(host_name, bdate):
  s = select([client.c.name, job.c.name, job.c.jobstatus, job.c.schedtime, job.c.jobfiles, job.c.jobbytes, job.c.jobid, job.c.level, job.c.starttime, job.c.endtime],  use_labels=True).where(and_(client.c.clientid == job.c.clientid, cast(job.c.schedtime,Date) == bdate, job.c.name == host_name, job.c.schedtime == bdate))
  _short_res = db.execute(s).fetchall()
  short_res = []
  for i, _short in enumerate(_short_res):
    c_name = _short[0]
    j_name = _short[1]
    j_status = _short[2]
    j_schedtime = _short[3]
    j_files = _short[4]
    j_bytes = _short[5]
    j_id = _short[6]
    j_level = _short[7]
    j_start = _short[8]
    j_end = _short[9]
    f_sel = select([path.c.path, filename.c.name, files.c.lstat]).where(
        and_(
            job.c.name == host_name,
            job.c.jobid == files.c.jobid,
            job.c.schedtime == bdate,
            filename.c.filenameid == files.c.filenameid,
            path.c.pathid == files.c.pathid
            )
        )
    f_res = db.execute(f_sel).fetchall()
    backup_files_list = []
    for record in f_res:
      backup_files_list.append(decode_file_info(record))
    short_res.append({
      'id': int(j_id),
      'cname': c_name,
      'jname': j_name,
      'jstatus': static_vars.JobStatus[j_status],
      'jschedtime': j_schedtime.strftime('%Y-%m-%d %H:%M:%S'),
      'jstarttime': j_start.strftime('%Y-%m-%d %H:%M:%S'),
      'jendtime': j_end.strftime('%Y-%m-%d %H:%M:%S'),
      'jduration': (j_end - j_start),
      'jdelay': (j_start - j_schedtime),
      'files': int(j_files),
      'size': sizeof_fmt(int(j_bytes)),
      'files_list': backup_files_list,
      'jlevel': static_vars.JobLevel[j_level],
    })
  s1 = select([client.c.name, job.c.name, job.c.schedtime, job.c.jobfiles, job.c.jobbytes],  use_labels=True).where(and_(client.c.clientid == job.c.clientid, jobhist.c.schedtime > date.today() - timedelta(days=14), job.c.name == host_name))
  s2 = select([client.c.name, jobhist.c.name.label('job_name'), jobhist.c.schedtime, jobhist.c.jobfiles, jobhist.c.jobbytes],  use_labels=True).where(and_(client.c.clientid == jobhist.c.clientid, jobhist.c.schedtime > date.today() - timedelta(days=14), jobhist.c.name == host_name))
  query = s1.union(s2).alias('job_name')
  result = db.execute(query).fetchall()
  b_s_res = []
  b_c_res = []
  for j, tmp in enumerate(result):
    k,x,y,z,i = tmp
    b_s_res.append( (k, y, i) )
    b_c_res.append( (k, y, z) )
  b_s_result = b_c_result = []
  b_s_result = gen_chart_array_time_3d(b_s_res)
  b_c_result = gen_chart_array_time_3d(b_c_res)
  return render_template("client.html", title='Detailed information for '+host_name, short_info=short_res, query=s, size_result=b_s_result, fcount_result=b_c_result)

@app.route('/reports/long_running_backup', methods=['POST'])
def long_running_backups():
  s = select([
      client.c.name,
      job.c.name,
      job.c.jobstatus,
      job.c.schedtime,
      job.c.starttime,
      job.c.endtime,
      job.c.jobfiles,
      job.c.jobbytes,
      job.c.jobid
    ]).where(
    and_(
      job.c.schedtime > datetime.now() - timedelta(hours=24),
      client.c.clientid == job.c.clientid,
      job.c.starttime + timedelta(minutes=30) < job.c.endtime
      )
    )
  result = db.execute(s).fetchall()
  long_job = []
  for j, tmp in enumerate(result):
    cname = tmp[0]
    jname = tmp[1]
    jstatus = tmp[2]
    jsched = tmp[3]
    jstart = tmp[4]
    jend = tmp[5]
    jfiles = tmp[6]
    jbytes = tmp[7]
    jid = tmp[8]
    jduration = jend - jstart
    long_job.append({
      'cname': cname,
      'jname': jname,
      'jstatus': static_vars.JobStatus[jstatus],
      'jsched': jsched.strftime('%Y-%m-%d %H:%M:%S'),
      'jstart': jstart.strftime('%Y-%m-%d %H:%M:%S'),
      'jend': jend.strftime('%Y-%m-%d %H:%M:%S'),
      'jduration': jduration,
      'jfiles': int(jfiles),
      'jbytes': sizeof_fmt(int(jbytes)),
      'jid': int(jid),
    })
  return render_template('long_running_backups.html', title="Backups which run more than 30 minutes", long_job=long_job)

@app.route('/reports/old_volumes')
def old_volumes():
  vol_list = {}
  s = """
  select
    p.name,
    p.poolid,
    p.volretention,
    p.pooltype,
    p.maxvols,
    p.numvols
  from
    pool as p
  """
  pools = db.execute(s).fetchall()
  for i, pool in enumerate(pools):
    _pool = { str(pool[0]) : { 'ppid': int(pool[1]), 'pvolret': int(pool[2]), 'pptype': str(pool[3]), 'pmvol': int(pool[4]), 'pnumvol': int(pool[5]), 'vols': {} } }
    st = """
    select 
      m.volumename,
      m.mediatype,
      m.volstatus,
      m.lastwritten,
      m.volretention,
      extract(epoch from (select (now() - m.lastwritten)))
    from
      media as m
    where
      m.poolid = """ + str(_pool[pool[0]]['ppid'])
    medias = db.execute(st).fetchall()
    _media = {}
    for j, media in enumerate(medias):
      if media[3] != None:
        mlastwr = media[3].strftime('%Y-%m-%d %H:%M:%S')
      else:
        mlastwr = "Never used"
      if media[5] != None:
        mlastdiff = int(media[5])
      else:
        mlastdiff = int(media[4])
      _media.update({ str(media[0]) : { 'mtype': str(media[1]), 'mvolst': static_vars.VOLUME_STATUS_SEVERITY[str(media[2])], 'mlastwr': mlastwr, 'mvolret': int(media[4]), 'mlastdiff': mlastdiff } })
    _pool[pool[0]]['vols'] = _media
    vol_list.update(_pool)
  return render_template('old_volumes.html', title="Not recycled volumes report", vol_list=vol_list)

@app.route('/reports/backup_duration/<bddate>', methods=['GET', 'POST'])
def backup_duration(bddate):
  s = select([pool.c.name, func.min(job.c.starttime), func.max(job.c.endtime)],  use_labels=True).where(and_(job.c.poolid == pool.c.poolid, cast(job.c.schedtime,Date) <= datetime.fromtimestamp(float(bddate)), cast(job.c.schedtime,Date) >= datetime.fromtimestamp(float(bddate)) - timedelta(days=1))).group_by(pool.c.name, job.c.schedtime)
  bd = db.execute(s).fetchall()
  bd_result = {}
  for bpool in bd:
    bd_result.update({ bpool[0]: { 'start': bpool[1], 'end': bpool[2] } })
  s = select([func.min(job.c.starttime), func.max(job.c.endtime)],  use_labels=True).where(job.c.poolid == pool.c.poolid)
  _min_date, _max_date = db.execute(s).fetchone()
  min_date = int(mktime((strptime(str(_min_date), "%Y-%m-%d %H:%M:%S"))))
  max_date = int(mktime((strptime(str(_max_date), "%Y-%m-%d %H:%M:%S"))))
  return render_template('backup_duration.html', title="Backup duration time", bd_result=bd_result, bddate=int(bddate), min_date=min_date, max_date=max_date)

@app.route('/<fname>.html')
def show_file(fname):
  if fname == 'index':
    return redirect("/", code=302)
  else:
    fi = open(custom_path+fname+".html", 'r')
    text = fi.read()
    title = re.compile('<title>(.*?)</title>', re.DOTALL |  re.IGNORECASE).findall(text)
    text = re.sub("<head>.*?</head>", "", text, flags=re.DOTALL)
    text = re.sub("<(html|body)>", "", text, flags=re.DOTALL)
    text = re.sub("</(html|body)>", "", text, flags=re.DOTALL)
    return render_template('static_files.html', title=''.join(title), text=text)
