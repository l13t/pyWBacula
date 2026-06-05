import os
import urllib.request

ASSETS = [
    (
        "https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js",
        "app/static/chart.js",
    ),
    (
        "https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns@3.0.0/dist/chartjs-adapter-date-fns.bundle.min.js",
        "app/static/chartjs-adapter-date-fns.bundle.js",
    ),
    (
        "https://cdn.jsdelivr.net/npm/tablesort@5.3.0/dist/tablesort.min.js",
        "app/static/tablesort.js",
    ),
    (
        "https://cdn.jsdelivr.net/npm/tablesort@5.3.0/dist/sorts/tablesort.date.min.js",
        "app/static/sorts/tablesort.date.js",
    ),
    (
        "https://cdn.jsdelivr.net/npm/tablesort@5.3.0/dist/sorts/tablesort.dotsep.min.js",
        "app/static/sorts/tablesort.dotsep.js",
    ),
    (
        "https://cdn.jsdelivr.net/npm/tablesort@5.3.0/dist/sorts/tablesort.filesize.min.js",
        "app/static/sorts/tablesort.filesize.js",
    ),
    (
        "https://cdn.jsdelivr.net/npm/tablesort@5.3.0/dist/sorts/tablesort.number.min.js",
        "app/static/sorts/tablesort.number.js",
    ),
    (
        "https://cdn.jsdelivr.net/npm/tablesort@5.3.0/dist/sorts/tablesort.monthname.min.js",
        "app/static/sorts/tablesort.monthname.js",
    ),
    (
        "https://cdnjs.cloudflare.com/ajax/libs/jquery.address/1.6/jquery.address.min.js",
        "app/static/jquery.address.js",
    ),
]


def fetch_if_missing():
    for url, dest in ASSETS:
        if os.path.exists(dest):
            continue
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        try:
            urllib.request.urlretrieve(url, dest)
        except Exception as e:
            print(f"[fetch_assets] WARNING: could not fetch {dest}: {e}")
