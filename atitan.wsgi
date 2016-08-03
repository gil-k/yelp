#!/usr/bin/python
import sys
import logging

activate_this = '/home/ubuntu/atitan/BASELINE/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/ubuntu/atitan//")

from atitan import app as application
