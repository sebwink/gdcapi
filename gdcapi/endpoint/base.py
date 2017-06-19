import os
import json

import requests

from gdcapi.query import GdcApiQuery
from gdcapi.fields import GdcApiField
from gdcapi.groups import GdcApiGroup

class GdcApiCouldNotInitializeEndpoint(Exception):
    pass

class GdcApiQueryFailed(Exception):
    pass

class GdcEndpoint(object):

    _mapping = {}

    def __init__(self, api_root, name):
        self._name = name
        self.endpoint = api_root+'/'+name
        if name in {'annotations', 'cases', 'files', 'projects'}:
            self._mapping = self._get_mapping(self.endpoint)
        self._defaults = self._mapping.get('defaults', [])
        self._fields = self._mapping.get('fields', [])
        self._groups = self._mapping.get('expand', [])
        self._nested = self._mapping.get('nested', [])
        self._multi = self._mapping.get('multi', [])   # for GDC internal use

        if name in {'annotations', 'cases', 'files', 'projects'}:
            self._parse_mapping_tree()

    def _get_mapping(self, endpoint):
        response = requests.get(endpoint+'/_mapping')
        if response.status_code != 200:
            raise GdcApiCouldNotInitializeEndpoint
        return response.json()

    def _parse_mapping_tree(self):

        def split_into_parent_and_child(path):
            split = path.split('.')
            if len(split) == 1:
                return path, None
            return '.'.join(split[:-1]), split[-1]

        self._groups.sort()
        self._fields.sort()

        for group in self._groups:
            parent, child = split_into_parent_and_child(group)
            if not child:
                self.__dict__[parent] = GdcApiGroup(parent)
            else:
                eval('self.'+parent).__dict__[child] = GdcApiGroup(group)
                eval('self.'+parent)._groups.append(child)

        for field in self._fields:
            parent, child = split_into_parent_and_child(field)
            default = {'field': field, 'full': self._name+'.'+field}
            mapping = self._mapping['_mapping'].get(self._name+'.'+field, default)
            if not child:
                self.__dict__[parent] = GdcApiField(mapping)
            else:
                eval('self.'+parent).__dict__[child] = GdcApiField(mapping)
                eval('self.'+parent)._fields.append(child)

    def get_field(self, name):
        if name not in self._fields:
            return None
        return eval('self.'+name)

    def get_group(self, name):
        if name not in self._groups:
            return None
        return eval('self.'+name)

    @property
    def fields(self):
        return self._fields

    @property
    def groups(self):
        return self._groups

    @property
    def mapping(self):
        return self._mapping

    def query(self, query={}):
        # --- query of GdcApiQuery
        if isinstance(query, GdcApiQuery):
            query = query.as_json()
        # --- Empty query with GET
        if not query:
            response = requests.get(self.endpoint)
            if response.status_code != 200:
                raise GdcApiQueryFailed
            return response.json()
        # --- Non-empty query with POST
        as_json = False
        if query.get('format', 'json').lower() == 'json':
            as_json = True
        print(query)
        response = requests.post(self.endpoint,
                                 json=query,
                                 headers = {'Content-Type' : 'application/json'})
        if response.status_code != 200:
            print(response.content.decode('utf-8'))
            print(response.url)
            print(response.reason)
            raise GdcApiQueryFailed
        if as_json:
            return response.json()
        else:
            return response
