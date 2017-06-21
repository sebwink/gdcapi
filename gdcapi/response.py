
class GdcApiResponse(object):

    def __init__(self, json_response, query, endpoint, field_defaults):
        self._endpoint = endpoint.split('/')[-1]
        self._api_root = endpoint.split('/'+self._endpoint)[0]
        self._defaults = field_defaults
        if not 'data' in json_response.keys():
            raise InvalidResponse
        self._query = query
        self._warnings = json_response['warnings']
        self._hits = json_response['data']['hits']
        self._set_nodes_as_attributes()
        self._pagination = json_response['data']['pagination']
        self._count = self._pagination['count']
        self._from = self._pagination['from']
        self._pages = self._pagination['pages']
        self._size = self._pagination['size']
        self._sort = self._pagination['sort']
        self._total = self._pagination['total']
        self._aggregations = json_response['data'].get('aggregations', {})
        self._histograms = {
                             aggregation : { bucket['key'] : bucket['doc_count']
                                             for bucket in self._aggregations[aggregation]['buckets'] }
                             for aggregation in self._aggregations
                           }

    @property
    def histograms(self):
        return self._histograms

    @property
    def aggregations(self):
        return self._aggregations

    class GdcApiNodeValues(object):
        def __init__(self, name):
            self._name = name

        @property
        def name(self):
            return self._name

    class GdcApiGroupValues(GdcApiNodeValues):
        def __init__(self, name, children):
            super().__init__(name)
            self._children = children

        def __call__(self):
            return {
                     child : eval('self.'+self.name+'.'+child)()
                     for child in self.children
                   }

        @property
        def children(self):
            return self._children

    class GdcApiFieldValues(GdcApiNodeValues):
        def __init__(self, name, hits):
            super().__init__(name)
            self._hits = hits

        def __call__(self):
            def get_value(hit, keys):
                for key in keys:
                    if isinstance(hit, list):
                        hit = [h[key] for h in hit]
                    else:
                        hit = hit[key]
                return hit

            keys = self._name.split('.')
            return [get_value(hit, keys) for hit in self.hits]

        @property
        def hits(self):
            return self._hits

    def _set_nodes_as_attributes(self):
        def split_into_parent_and_child(path):
            split = path.split('.')
            if len(split) == 1:
                return path, None
            return '.'.join(split[:-1]), split[-1]

        def get_children(parent, groups, fields):
            children = {group for group in groups if group.startswith(parent)}
            return children | {field for field in fields if field.startswith(parent)}

        if 'fields' in self.query:
            fields = self.query['fields'].split(',')
        else:
            fields = self._defaults
        if 'expand' in self.query:
            groups = self.query['expand'].split(',')
        else:
            groups = []
        groups = set(groups)
        for field in fields:
            nodes = field.split('.')
            groups |= {'.'.join(nodes[:i+1]) for i in range(len(nodes))}
        groups = list(groups)

        groups.sort()
        fields.sort()
        # --- group value attributes
        for group in groups:
            parent, child = split_into_parent_and_child(group)
            children = get_children(parent, groups, fields)
            if not child:
                self.__dict__[parent] = self.GdcApiGroupValues(group, children)
            else:
                eval('self.'+parent).__dict__[child] = self.GdcApiGroupValues(group, children)
        # --- field value attributes
        for field in fields:
            parent, child = split_into_parent_and_child(field)
            if not child:
                self.__dict__[parent] = self.GdcApiFieldValues(field,
                                                               self.hits)
            else:
                eval('self.'+parent).__dict__[child] = self.GdcApiFieldValues(field,
                                                                              self.hits)

    def values(self, node):
        return eval('self.'+node)()

    @property
    def endpoint(self):
        return self._endpoint

    @property
    def api_root(self):
        return self._api_root

    @property
    def query(self):
        return self._query

    @property
    def warnings(self):
        return self._warnings

    @property
    def hits(self):
        return self._hits

    @property
    def pagination(self):
        return self._pagination

    @property
    def count(self):
        return self._count

    @property
    def from_page(self):
        return self._from

    @property
    def pages(self):
        return self._pages

    @property
    def size(self):
        return self._size

    @property
    def sort(self):
        return self._sort

    @property
    def total(self):
        return self._total
