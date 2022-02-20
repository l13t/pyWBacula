from time import gmtime, strftime

from app.db import db
import pandas as pd
import json
import plotly
import plotly.express as px
import libs.static_vars as static_vars


def application_data():
    return static_vars.app_info


def db_available():
    try:
        db.execute('select 1')
        return True, "DB works"
    except  Exception as e:
        return False, "DB problems: " + e
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


def gen_plotly(in_data):
    client_data = []
    date_data = []
    real_data = []
    for x, y, z in in_data:
        client_data.append(x)
        date_data.append(y.strftime('%Y-%m-%d %H:%M:%S'))
        real_data.append(z)
    return [client_data, date_data, real_data]


def gen_graph_json(ids, input_data, graph_name):
    graph_dict = dict(zip(ids, gen_plotly(input_data)))
    plot_dict = pd.DataFrame(graph_dict)
    figure_dict = px.line(plot_dict, x=ids[1], y=ids[2], color=ids[0], title=graph_name, markers=True)
    outJSON = json.dumps(figure_dict, cls=plotly.utils.PlotlyJSONEncoder)
    return outJSON


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
