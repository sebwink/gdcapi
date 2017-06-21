import os
import json

import requests

from gdcapi.query import GdcApiQuery, GdcApiQueryFilter
from gdcapi.fields import GdcApiField
from gdcapi.groups import GdcApiGroup
from gdcapi.response import GdcApiResponse


DEFAULT_API_ROOT = 'https://api.gdc.cancer.gov'

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
                self.__dict__[parent] = GdcApiField(mapping, self)
            else:
                eval('self.'+parent).__dict__[child] = GdcApiField(mapping, self)
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

    def query(self,
              query=None,
              fields = None,
              expand = None,
              facets = None,
              sort = None,
              size = None,
              from_page = None,
              response_format = None,
              filters = None,
              raw_json = False,
              get_all = False):
        if not query:
            query = {}
        if isinstance(query, GdcApiField):
            query = query()
        if isinstance(query, GdcApiQueryFilter):
            filters = query
            query = GdcApiQuery()
            query.filters = filters 
        # --- query of GdcApiQuery
        if isinstance(query, GdcApiQuery):
            query = query.as_json()
        # overwrite arguments
        if size is not None:
            query['size'] = size
        if from_page is not None:
            query['from_page'] = from_page
        if response_format:
            query['format'] = response_format
        if filters:
            query['filters'] = filters.filter
        if fields:
            if not isinstance(fields, list):
                fields = [fields]
            query['fields'] = ','.join([field.name for field in fields 
                                                   if isinstance(field, GdcApiField)])
        if expand:
            if not isinstance(expand, list):
                expand = [expand]
            query['expand'] = ','.join([group.name for group in expand
                                                   if isinstance(group, GdcApiGroup)])
        if facets:
            query['facets'] = ','.join([field.name for field in facets
                                                   if isinstance(field, GdcApiField)])
        if sort:
            query['sort'] = sort    #    TODO: formalize sort
        # --- get all hits
        if get_all:
            query['size'] = self.how_many(query.get('filters', {}))

        print(query)
        # --- Empty query with GET
        if not query:
            response = requests.get(self.endpoint)
            if response.status_code != 200:
                raise GdcApiQueryFailed
            if raw_json:
                return response.json()
            else:
                return GdcApiResponse(response.json(), query, self.endpoint, self._defaults)
        # --- Non-empty query with POST
        as_json = False
        if query.get('format', 'json').lower() == 'json':
            as_json = True
        response = requests.post(self.endpoint,
                                 json=query,
                                 headers = {'Content-Type' : 'application/json'})
        if response.status_code != 200:
            print(response.content.decode('utf-8'))
            print(response.url)
            print(response.reason)
            raise GdcApiQueryFailed
        if as_json:
            if raw_json:
                return response.json()
            return GdcApiResponse(response.json(), query, self.endpoint, self._defaults)
        else:
            return response

    def __call__(self, *args, **kwargs):
        return self.query(*args, **kwargs)

    def how_many(self, filters={}):
        response = self.query(filters, size=0)
        return response.total

    def get_all(self, *args, **kwargs):
        return self.query(*args, get_all=True, **kwargs)
