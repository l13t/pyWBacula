#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__credits__ = ["Dmytro Prokhorenkov"]
__version__ = "0.1"
__maintainer__ = "Dmytro Prokhorenkov"
__email__ = "liet@liet.kiev.ua"
__status__ = "Development"

from app import webapp
from flask_debug import Debug
import os

if __name__ == '__main__':
    DEBUG = bool(os.getenv("PWB_DEBUG", default="False"))
    PORT = os.getenv("PWB_PORT", default="15995")
    Debug(webapp)
    webapp.config['FLASK_DEBUG_DISABLE_STRICT'] = True
    webapp.run(host='0.0.0.0', port=PORT, debug=DEBUG, use_debugger=DEBUG, use_reloader=DEBUG)
