#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import webapp
from flask_debug import Debug
import os

if __name__ == '__main__':
    DEBUG = bool(os.getenv("PWB_DEBUG", default="False"))
    PORT = os.getenv("PWB_PORT", default="15995")
    HOST = os.getenv("PWB_HOST", default="127.0.0.1")
    Debug(webapp)
    webapp.config['FLASK_DEBUG_DISABLE_STRICT'] = True
    webapp.run(host=HOST, port=PORT, debug=DEBUG, use_debugger=DEBUG, use_reloader=DEBUG)
