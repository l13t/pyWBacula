from datetime import datetime
from time import gmtime, strftime
import json

from app.db import db
import libs.static_vars as static_vars

CHART_PALETTE = [
    '#42a5f5', '#ef5350', '#66bb6a', '#ab47bc',
    '#26a69a', '#ffa726', '#78909c', '#ec407a',
]


def application_data():
    return static_vars.app_info


def db_available():
    try:
        db.execute('select 1')
        return True, "DB works"
    except Exception as e:
        return False, "DB problems: " + str(e)
    # try:
    #     db.session.query("1").from_statement("SELECT 1").all()
    #     return True, "DB works"
    # except:
    #     return False, "DB problems"


def gen_chart_array_time_3d(in_data):
    tmp_result = {}
    for x, y, z in in_data:
        try:
            tmp_result[str(x)].update(dict([(y.strftime('%Y-%m-%d %H:%M:%S'),
                                             int(z))]))
        except KeyError:
            tmp_result[str(x)] = dict([(y.strftime('%Y-%m-%d %H:%M:%S'),
                                        int(z))])
    last_result = []
    for res_key, res_val in tmp_result.items():
        temp = dict([('name', res_key), ('data', res_val)])
        last_result.append(temp)
    return last_result


def gen_graph_json(ids, input_data, graph_name):
    grouped = {}
    for row in input_data:
        group = str(row[0])
        x = row[1].strftime('%Y-%m-%dT%H:%M:%S') if isinstance(row[1], datetime) else str(row[1])
        y = int(row[2]) if row[2] is not None else 0
        grouped.setdefault(group, []).append({'x': x, 'y': y})
    datasets = []
    for i, (label, data) in enumerate(grouped.items()):
        color = CHART_PALETTE[i % len(CHART_PALETTE)]
        datasets.append({
            'label': label,
            'data': data,
            'borderColor': color,
            'backgroundColor': color + '33',
            'fill': False,
            'tension': 0.1,
            'pointRadius': 3,
        })
    return json.dumps({'datasets': datasets, 'title': graph_name})


def base64_decode_lstat(record, position):
    b64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    val = 0
    size = record.split(' ')[position]
    for i in range(len(size)):
        val += (b64.find(size[i])) * (pow(64, (len(size) - i) - 1))
    return val


def decode_file_info(record):
    return_array = {}
    file_name = record[0] + record[1]
    atime = gmtime(base64_decode_lstat(record[2], 10))
    mtime = gmtime(base64_decode_lstat(record[2], 11))
    ctime = gmtime(base64_decode_lstat(record[2], 12))
    return_array = {'fname': file_name,
                    'uid': base64_decode_lstat(record[2], 6),
                    'gid': base64_decode_lstat(record[2], 5),
                    'size': sizeof_fmt(base64_decode_lstat(record[2], 7)),
                    'mtime': strftime("%b %d %Y %H:%M", mtime),
                    'atime': strftime("%b %d %Y %H:%M", atime),
                    'ctime': strftime("%b %d %Y %H:%M", ctime),
                    'real_size': base64_decode_lstat(record[2], 7)
                    }
    return return_array


def show_decoded_big_files_results(result, f_size):
    return_array = []
    for record in result:
        if (base64_decode_lstat(record[2], 7) > f_size * 1024 * 1024):
            return_array.append(decode_file_info(record))
    return return_array


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.2f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f %s%s" % (num, 'Yi', suffix)
