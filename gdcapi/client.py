import os
import shutil
import subprocess
import getpass

__mypath__ = os.path.dirname(os.path.abspath(__file__))

class GdcClient(object):

    def __init__(self, path=None):
        if not path:
            path = shutil.which('gdc-client')
        self.client = path

    def run(self, command=None,
                  stdout=None,
                  stderr=None,
                  *pargs,
                  **kwargs):
        if not self.client:
            print('Cannot find gdc-client...')
            return None
        args = []
        for option in kwargs:
            args += ['--'+option, kwargs[option]]
        args += pargs
        if command:
            args = [command, *args]
        return subprocess.Popen([self.client] + args, stdout=stdout, stderr=stderr)


    def help(self, command=None):
        return self.run(command, None, None, '--help')

