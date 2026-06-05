bind = "0.0.0.0:15995"
workers = 4
timeout = 90
accesslog = "-"
errorlog = "-"
access_log_format = (
    '{"ts":"%(t)s","method":"%(m)s","path":"%(U)s%(q)s",'
    '"status":%(s)s,"bytes":%(b)s,"duration_ms":%(D)s}'
)
