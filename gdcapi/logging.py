import os
import json

default_log_file=os.path.expanduser('~/.gdcapi/log/default.log')
default_log_dir=os.path.dirname(default_log_file)

if not os.path.isdir(default_log_dir):
    os.makedirs(default_log_dir)

class Logger(object):
    def __init__(self, fp):
        self.logfile = fp

    def log(self, endpoint, query):
        if not self.logfile:
            return
