import os
import json

import requests

import gdcapi.logging

__mypath__ = os.path.dirname(os.path.abspath(__file__))

class GdcApiQueryFailed(Exception):
    pass

class GdcEndpoint(object):

    _fields = None
    _field_groups = None

    def __init__(self, api_root, name, log_fp=None):
        self.endpoint = api_root+'/'+name
        self.logger = gdcapi.logging.Logger(log_fp)
        self._read_fields(name)
        self._read_field_groups(name)

    def _read_field_info(self, name, what):
        _file = os.path.join(__mypath__, os.path.join('data', what+'/'+name+'.txt'))
        if os.path.isfile(_file):
            with open(_file, 'r') as this:
                return {line.strip() for line in this.readlines() if line.strip()}

    def _read_fields(self, name):
        self._fields = self._read_field_info(name, 'fields')

    def _read_field_groups(self, name):
        self._groups = self._read_field_info(name, 'groups')

    @property
    def fields(self):
        return self._fields

    @property
    def groups(self):
        return self._groups

    def query(self, query={}, as_json=True):
        query = {
                  key : json.dumps(query[key])
                  for key in query
                  if not isinstance(query[key], str)
                }
        self.logger.log(self.endpoint, query)
        response = requests.get(self.endpoint, params=query)
        if response.status_code != 200:
            raise GdcApiQueryFailed
        if as_json:
            return response.json()
        else:
            return response


class Status(GdcEndpoint):
    def __init__(self, api_root, log_fp):
        super().__init__(api_root, 'status', log_fp)


class Projects(GdcEndpoint):
    def __init__(self, api_root, log_fp):
        super().__init__(api_root, 'projects', log_fp)


class Cases(GdcEndpoint):
    def __init__(self, api_root, log_fp):
        super().__init__(api_root, 'cases', log_fp)


class Files(GdcEndpoint):
    def __init__(self, api_root, log_fp):
        super().__init__(api_root, 'files', log_fp)


class Annotations(GdcEndpoint):
    def __init__(self, api_root, log_fp):
        super().__init__(api_root, 'annotations', log_fp)


class Data(GdcEndpoint):
    def __init__(self, api_root, log_fp):
        super().__init__(api_root, 'data', log_fp)


class Manifest(GdcEndpoint):
    def __init__(self, api_root, log_fp):
        super().__init__(api_root, 'manifest', log_fp)


class Slicing(GdcEndpoint):
    def __init__(self, api_root, log_fp):
        super().__init__(api_root, 'slicing', log_fp)


class Submission(GdcEndpoint):
    def __init__(self, api_root, log_fp):
        super().__init__(api_root, 'submission', log_fp)
