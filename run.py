#!/usr/bin/env python
# -*- coding: utf-8 -*-

__credits__ = [ "Dmytro Prokhorenkov" ]
__version__ = "0.1"
__maintainer__ = "Dmytro Prokhorenkov"
__email__ = "liet@liet.kiev.ua"
__status__ = "Development"

from app import app

if __name__ == '__main__':
  #app.run(host='0.0.0.0', port=15995, debug = True)
  app.run(host='0.0.0.0', port=15995, debug = False)
