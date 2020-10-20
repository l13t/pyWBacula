#!/usr/bin/env python
# -*- coding: utf-8 -*-

__credits__ = ["Dmytro Prokhorenkov"]
__version__ = "0.1"
__maintainer__ = "Dmytro Prokhorenkov"
__email__ = "liet@liet.kiev.ua"
__status__ = "Development"

from app import app
import os

if __name__ == '__main__':
    DEBUG = os.getenv(PWB_DEBUG, default=False)
    PORT = os.getenv(PWB_PORT, default=15995)
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
