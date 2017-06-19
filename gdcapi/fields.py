import functools

import gdcapi.query

def get_filter(operator):

    @functools.wraps(operator)
    def wrapper(self, *args, **kwargs):
        _filter = gdcapi.query.GdcApiQueryFilter()
        _filter._filter = operator(self, *args, **kwargs)
        return _filter

    return wrapper


class GdcApiField(object):
    def __init__(self, mapping):
        self._description = mapping.get('description', None)
        if self._description:
            self._description = self._description.strip()
        self._doc_type = mapping.get('doc_type', None)
        self._field = mapping.get('field', None)
        self._full = mapping.get('full', None)
        self._type = mapping.get('type', None)

    @property
    def name(self):
        return self._field

    @property
    def description(self):
        return self._description

    @property
    def doc_type(self):
        return self._doc_type

    @property
    def field(self):
        return self._field

    @property
    def full(self):
        return self._full

    @property
    def type(self):
         return self._type

    def __hash__(self):
        return self._full.__hash__()

    def __call__(self):
        return self._existence_filter('not')

    def __invert__(self):
        return self._existence_filter('is')

    @get_filter
    def _existence_filter(self, op):
        return {
                 'op'      : op,
                 'content' : {'field' : self.full }
               }

    def __eq__(self, other):
        return self._binary_cmp_filter(other, '=')

    def __ne__(self, other):
        return self._binary_cmp_filter(other, '!=')

    def __lt__(self, other):
        return self._binary_cmp_filter(other, '<')

    def __le__(self, other):
        return self._binary_cmp_filter(other, '<=')

    def __gt__(self, other):
        return self._binary_cmp_filter(other, '>')

    def __ge__(self, other):
        return self._binary_cmp_filter(other, '>=')

    @get_filter
    def _binary_cmp_filter(self, other, op):
        return {
                 'op'      : op,
                 'content' : {
                               'field' : self.full,
                               'value' : str(other)
                             }
                }

    def __rshift__(self, other):
        return self._array_filter(other, 'in')

    def __sub__(self, other):
        return self._array_filter(other, 'exclude')

    @get_filter
    def _array_filter(self, other, op):
        other = set(other)
        return {
                 'op'      : op,
                 'content' : {
                               'field' : self.full,
                               'value' : [str(e) for e in other]
                             }
               }
