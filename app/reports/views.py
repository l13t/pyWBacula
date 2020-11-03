from datetime import datetime, date, timedelta
from flask import Blueprint, render_template, request, redirect, send_from_directory
from sqlalchemy import cast, Date
from sqlalchemy.sql import and_, select, func
from time import gmtime, strptime, mktime
from libs import pwb, static_vars
from app.db import db
import config
import os
import re

reports = Blueprint('reports', __name__)

custom_path = config.CUSTOM_PATH

@reports.route('/reports', methods=['GET'])
def show_reports():
    unix_today = int(mktime(gmtime()))
    return render_template('reports.html', title='Available reports list', unix_date=unix_today)


@reports.route('/reports/jobs', methods=['POST'])
def jobs_report():
    s = """
    SELECT
        client.name AS client_name, job.name AS job_name, job.jobstatus AS job_jobstatus,
        job.starttime AS job_startime, job.endtime AS job_endtime, job.schedtime AS job_schedtime,
        job.jobfiles AS job_jobfiles, job.jobbytes AS job_jobbytes, job.level as job_level
    FROM
        client, job, (select max(job.schedtime) as max_schedtime, job.name AS job_name from job group by job.name) as lj
    WHERE
        lj.job_name = job.name and job.schedtime = lj.max_schedtime and client.clientid = job.clientid"""
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
            'jbytes': pwb.sizeof_fmt(int(jbytes)),
            'jlevel': static_vars.JobLevel[jlevel],
            'old_job': old_job,
        })
    return render_template('jobs_report.html',
                           title='Jobs report',
                           jobs=result)


@reports.route('/reports/big_files', methods=['GET', 'POST'])
def big_files_report():
    # _max_size = 10
    # if request.method == 'POST':
    #     _max_size = int(request.form['_max_size'])
    #s = select([job.c.name, job.c.schedtime]).where(job.c.schedtime > datetime.now() - timedelta(hours=24))
    query = """
    SELECT
        name, schedtime
    FROM
        job
    WHERE
        job.schedtime > NOW() - INTERVAL '24 hours'
    """
    result = db.execute(query).fetchall()
    proceed_result = {}
    sched_time = {}
    for res in result:
        job_i = str(res[0])
        # s = select([path.c.path, filename.c.name, files.c.lstat]).where(
        #     and_(job.c.name == job_i,
        #          job.c.jobid == files.c.jobid,
        #          job.c.schedtime > datetime.now() - timedelta(hours=24),
        #          filename.c.filenameid == files.c.filenameid,
        #          path.c.pathid == files.c.pathid
        #          ))
        query = """
        SELECT
            path.path, filename.name, file.lstat
        FROM
            path, filename, file, job
        WHERE
            job.name = '{}' AND job.jobid = file.jobid AND path.pathid = file.pathid AND
            filename.filenameid = file.filenameid AND job.schedtime > NOW() - INTERVAL '24 hours'
        """.format(job_i)
        out_res = db.execute(query)
        proceed_result[job_i] = pwb.show_decoded_big_files_results(out_res, 10)
        sched_time[job_i] = res[1].strftime("%Y-%m-%d %H:%M:%S")
    return render_template('bigfiles_report.html',
                           title='Big files report',
                           bf_report=proceed_result,
                           res=result,
                           sched_time=sched_time)


@reports.route('/reports/pool_size_report', methods=['POST'])
def pool_size_report():
    s = """
    SELECT
        pool_name, job_schedtime, sum(pool_size) as pool_size
    FROM (
        SELECT
            pool.name as pool_name, date_trunc('day', job.schedtime) as job_schedtime, job.jobbytes as pool_size
        FROM
            pool, job
        WHERE
            date_trunc('day', job.schedtime) > now() - interval '28 days' and job.poolid = pool.poolid
        UNION
            SELECT
                pool.name as pool_name, date_trunc('day', jobhisto.schedtime) as job_schedtime, jobhisto.jobbytes as pool_size
            FROM
                pool, jobhisto
            WHERE
                date_trunc('day', jobhisto.schedtime) > now() - interval '28 days' and jobhisto.poolid = pool.poolid
        ORDER BY
            job_schedtime, pool_name) as foo
    GROUP BY
        pool_name, job_schedtime
    ORDER BY
        job_schedtime, pool_name;
    """
    result = db.execute(s).fetchall()
    s_s_result = pwb.gen_chart_array_time_3d(result)
    return render_template("pool_size.html",
                           title='Pool size report',
                           s_size=s_s_result)


@reports.route('/reports/client/<host_name>/<bdate>', methods=['GET', 'POST'])
def client_detailed_info(host_name, bdate):
    # s = select([client.c.name,
    #             job.c.name,
    #             job.c.jobstatus,
    #             job.c.schedtime,
    #             job.c.jobfiles,
    #             job.c.jobbytes,
    #             job.c.jobid,
    #             job.c.level,
    #             job.c.starttime,
    #             job.c.endtime
    #             ],
    #            use_labels=True).where(and_(client.c.clientid == job.c.clientid,
    #                                        cast(job.c.schedtime, Date) == bdate,
    #                                        job.c.name == host_name,
    #                                        job.c.schedtime == bdate))
    query = """
    SELECT
        client.name, job.name, job.jobstatus, job.schedtime, job.jobfiles, job.jobid, job.level, job.starttime, job.endtime
    FROM
        job, client
    WHERE
        client.clientid = job.clientid AND job.name = {} AND job.schedtime = {}
    """.format(host_name, bdate)
    _short_res = db.execute(query).fetchall()
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
        # f_sel = select([path.c.path, filename.c.name, files.c.lstat]).where(
        #     and_(job.c.name == host_name,
        #          job.c.jobid == files.c.jobid,
        #          job.c.schedtime == bdate,
        #          filename.c.filenameid == files.c.filenameid,
        #          path.c.pathid == files.c.pathid
        #          ))
        f_sel = """
        SELECT
            path.path, filename.name, file.lstat
        FROM
            path, filename, file, job
        WHERE
            job.name = {} AND job.jobid = files.jobid NAD job.schedtime = {} AND filename.filenameid = file.filenameid AND path.pathid = file.pathid
        """.format(host_name, bdate)
        f_res = db.execute(f_sel).fetchall()
        backup_files_list = []
        for record in f_res:
            backup_files_list.append(pwb.decode_file_info(record))
        short_res.append({'id': int(j_id),
                          'cname': c_name,
                          'jname': j_name,
                          'jstatus': static_vars.JobStatus[j_status],
                          'jschedtime': j_schedtime.strftime('%Y-%m-%d %H:%M:%S'),
                          'jstarttime': j_start.strftime('%Y-%m-%d %H:%M:%S'),
                          'jendtime': j_end.strftime('%Y-%m-%d %H:%M:%S'),
                          'jduration': (j_end - j_start),
                          'jdelay': (j_start - j_schedtime),
                          'files': int(j_files),
                          'size': pwb.sizeof_fmt(int(j_bytes)),
                          'files_list': backup_files_list,
                          'jlevel': static_vars.JobLevel[j_level],
                          })
    s1 = select([client.c.name,
                 job.c.name,
                 job.c.schedtime,
                 job.c.jobfiles,
                 job.c.jobbytes],
                use_labels=True).where(and_(client.c.clientid == job.c.clientid,
                                            job.c.schedtime > date.today() - timedelta(days=14),
                                            job.c.name == host_name))
    s2 = select([client.c.name,
                 jobhist.c.name.label('job_name'),
                 jobhist.c.schedtime,
                 jobhist.c.jobfiles,
                 jobhist.c.jobbytes],
                use_labels=True).where(and_(client.c.clientid == jobhist.c.clientid,
                                            jobhist.c.schedtime > date.today() - timedelta(days=14),
                                            jobhist.c.name == host_name))
    query = s1.union(s2).alias('job_name')
    result = db.execute(query).fetchall()
    b_s_res = []
    b_c_res = []
    for j, tmp in enumerate(result):
        k, x, y, z, i = tmp
        b_s_res.append((k, y, i))
        b_c_res.append((k, y, z))
    b_s_result = b_c_result = []
    b_s_result = pwb.gen_chart_array_time_3d(b_s_res)
    b_c_result = pwb.gen_chart_array_time_3d(b_c_res)
    return render_template("client.html",
                           title='Detailed information for ' + host_name,
                           short_info=short_res,
                           query=s,
                           size_result=b_s_result,
                           fcount_result=b_c_result)


@reports.route('/reports/long_running_backup', methods=['POST'])
def long_running_backups():
    # s = select([client.c.name,
    #             job.c.name,
    #             job.c.jobstatus,
    #             job.c.schedtime,
    #             job.c.starttime,
    #             job.c.endtime,
    #             job.c.jobfiles,
    #             job.c.jobbytes,
    #             job.c.jobid]).where(and_(job.c.schedtime > datetime.now() - timedelta(hours=24),
    #                                      client.c.clientid == job.c.clientid,
    #                                      job.c.starttime + timedelta(minutes=30) < job.c.endtime))
    query = """
    SELECT
        client.name, job.name, job.jobstatus, job.schedtime, job.starttime, job.endtime, job.jobfiles, job.jobbytes, job.jobid
    FROM
        job, client
    WHERE
        job.schedtime > NOW() - INTERVAL '24 hours' AND client.clientid = job.clientid AND job.starttime + INTERVAL '30 minutes' < job.endtime
    """
    result = db.execute(query).fetchall()
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
        long_job.append({'cname': cname,
                         'jname': jname,
                         'jstatus': static_vars.JobStatus[jstatus],
                         'jsched': jsched.strftime('%Y-%m-%d %H:%M:%S'),
                         'jstart': jstart.strftime('%Y-%m-%d %H:%M:%S'),
                         'jend': jend.strftime('%Y-%m-%d %H:%M:%S'),
                         'jduration': jduration,
                         'jfiles': int(jfiles),
                         'jbytes': pwb.sizeof_fmt(int(jbytes)),
                         'jid': int(jid),
                         })
    return render_template('long_running_backups.html',
                           title="Backups which run more than 30 minutes",
                           long_job=long_job)


@reports.route('/reports/old_volumes', methods=['GET'])
def old_volumes():
    vol_list = {}
    s = """
    SELECT
        p.name,
        p.poolid,
        p.volretention,
        p.pooltype,
        p.maxvols,
        p.numvols
    FROM
        pool as p
    """
    pools = db.execute(s).fetchall()
    for i, pool in enumerate(pools):
        _pool = {str(pool[0]): {'ppid': int(pool[1]),
                                'pvolret': int(pool[2]),
                                'pptype': str(pool[3]),
                                'pmvol': int(pool[4]),
                                'pnumvol': int(pool[5]),
                                'vols': {}
                                }}
        st = """
        SELECT
            m.volumename,
            m.mediatype,
            m.volstatus,
            m.lastwritten,
            m.volretention,
            extract(epoch from (select (now() - m.lastwritten)))
        FROM
            media as m
        WHERE
            m.poolid = """ + str(_pool[pool[0]]['ppid'])

        medias = db.execute(st).fetchall()
        _media = {}
        for j, media in enumerate(medias):
            if media[3] is not None:
                mlastwr = media[3].strftime('%Y-%m-%d %H:%M:%S')
            else:
                mlastwr = "Never used"

            if media[5] is not None:
                mlastdiff = int(media[5])
            else:
                mlastdiff = int(media[4])

            _media.update({str(media[0]): {'mtype': str(media[1]),
                                           'mvolst': static_vars.VOLUME_STATUS_SEVERITY[str(media[2])],
                                           'mlastwr': mlastwr,
                                           'mvolret': int(media[4]),
                                           'mlastdiff': mlastdiff}})
        _pool[pool[0]]['vols'] = _media
        vol_list.update(_pool)
    return render_template('old_volumes.html', title="Not recycled volumes report", vol_list=vol_list)


@reports.route('/reports/backup_duration/<bddate>', methods=['GET', 'POST'])
def backup_duration(bddate):
    s = select([pool.c.name,
                func.min(job.c.starttime),
                func.max(job.c.endtime)],
               use_labels=True).where(and_(job.c.poolid == pool.c.poolid,
                                           cast(job.c.schedtime, Date) <= datetime.fromtimestamp(float(bddate)),
                                           cast(job.c.schedtime, Date) >= datetime.fromtimestamp(float(bddate)) - timedelta(days=1))).group_by(pool.c.name, job.c.schedtime)
    bd = db.execute(s).fetchall()
    bd_result = {}
    for bpool in bd:
        bd_result.update({bpool[0]: {'start': bpool[1], 'end': bpool[2]}})
    s = select([func.min(job.c.starttime),
                func.max(job.c.endtime)],
               use_labels=True).where(job.c.poolid == pool.c.poolid)
    _min_date, _max_date = db.execute(s).fetchone()
    min_date = int(mktime((strptime(str(_min_date), "%Y-%m-%d %H:%M:%S"))))
    max_date = int(mktime((strptime(str(_max_date), "%Y-%m-%d %H:%M:%S"))))
    return render_template('backup_duration.html',
                           title="Backup duration time",
                           bd_result=bd_result,
                           bddate=int(bddate),
                           min_date=min_date,
                           max_date=max_date)


@reports.route('/<fname>.html', methods=['GET'])
def show_file(fname):
    if fname == 'index':
        return redirect("/", code=302)
    else:
        fi = open(custom_path + fname + ".html", 'r')
        text = fi.read()
        title = re.compile('<title>(.*?)</title>', re.DOTALL | re.IGNORECASE).findall(text)
        text = re.sub("<head>.*?</head>", "", text, flags=re.DOTALL)
        text = re.sub("<(html|body)>", "", text, flags=re.DOTALL)
        text = re.sub("</(html|body)>", "", text, flags=re.DOTALL)
        return render_template('static_files.html', title=''.join(title), text=text)


@reports.route('/reports/media/<media>', methods=['GET', 'POST'])
def media_report(media):
    media_info_query = """
    SELECT
        m.volumename,
        p.name,
        p.labelformat,
        m.mediatype,
        m.firstwritten,
        m.lastwritten,
        m.labeldate,
        m.volbytes,
        m.volstatus,
        m.enabled,
        m.recycle,
        m.volretention,
        s.name,
        m.recyclecount
    FROM
        media as m,
        pool as p,
        storage as s
    WHERE
        p.poolid = m.poolid and
        m.storageid = s.storageid and
        m.volumename = '""" + media + """';
    """

    _media_info_result = db.execute(media_info_query).fetchone()
    media_info_result = {}
    media_info_result['volname'] = str(_media_info_result[0])
    media_info_result['poolname'] = str(_media_info_result[1])
    media_info_result['labelformat'] = str(_media_info_result[2])
    media_info_result['mediatype'] = str(_media_info_result[3])
    media_info_result['fwr'] = _media_info_result[4].strftime('%Y-%m-%d %H:%M:%S')
    media_info_result['lwr'] = _media_info_result[5].strftime('%Y-%m-%d %H:%M:%S')
    media_info_result['ldate'] = _media_info_result[6].strftime('%Y-%m-%d %H:%M:%S')
    media_info_result['volbytes'] = pwb.sizeof_fmt(int(_media_info_result[7]))
    media_info_result['volstatus'] = static_vars.VOLUME_STATUS_SEVERITY[str(_media_info_result[8])]
    media_info_result['enabled'] = str(_media_info_result[9])
    media_info_result['recycle'] = int(_media_info_result[10])
    media_info_result['volret'] = int(_media_info_result[11])
    media_info_result['storagename'] = str(_media_info_result[12])
    media_info_result['reccount'] = int(_media_info_result[13])

    job_inside_media_query = """
    SELECT
        j.name,
        j.schedtime,
        j.jobid,
        m.volumename
    FROM
        job as j,
        media as m,
        jobmedia as jm
    WHERE
        m.volumename = '""" + media + """' and
        m.mediaid = jm.mediaid and
        jm.jobid = j.jobid
    GROUP BY
        j.jobid,
        m.volumename;
    """

    job_inside_media_result = db.execute(job_inside_media_query).fetchall()
    job_inside_media_list = []

    for jiml_id, jiml_data in enumerate(job_inside_media_result):
        job_inside_media_list.append({'job_name': str(jiml_data[0]),
                                      'job_sched': jiml_data[1].strftime('%Y-%m-%d %H:%M:%S'),
                                      'jobid': int(jiml_data[2])})

    media_info_result['jobs'] = job_inside_media_list

    return render_template('media_report.html',
                           title="Detailed information about volume " + media,
                           mir=media_info_result)
