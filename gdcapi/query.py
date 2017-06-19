import itertools

from gdcapi.fields import GdcApiField
from gdcapi.groups import GdcApiGroup

class GdcApiQuery(object):
    _query_count = itertools.count(1)

    def __init__(self):
        self._id = next(self._query_count)
        self.filters = GdcApiQueryFilter()
        self._format = 'JSON'
        self._pretty = None
        self.fields = GdcApiFieldSet()
        self.expand = GdcApiGroupSet()
        self._size = 10
        self._from = 1
        self._sort = None
        self.facets = GdcApiFieldSet()

    @property
    def format(self):
        return self._format

    @property
    def pretty(self):
        return self._pretty

    @property
    def size(self):
        return self._size

    @property
    def from_page(self):
        return self._from

    @property
    def sort(self):
        return self._sort

    def as_json(self):

        if isinstance(self.filters, GdcApiField):
            _filter = self.filters()
        else:
            _filter = self.filters.filter

        json = { }

        if _filter:
            json['filters'] = _filter

        json['size'] = self._size
        json['from'] = self._from
        json['format'] = self._format

        if self._pretty:
            json['pretty'] = self._pretty

        if self._sort:
            json['sort'] = self._sort

        for key in {'fields', 'facets', 'expand'}:
            if self.__dict__[key]._set:
                json[key] = self.__dict__[key]._set
                json[key] = ','.join([e.name for e in json[key]])

        return json


class GdcApiNodeSet(object):
    
    def __init__(self, element_type):
        self._set = set()
        self._element_type = element_type

    def _type_check(self, item):
        if not isinstance(item, self._element_type):
            raise TypeError
        return item

    def _array_type_check(self, items):
        if not isinstance(items, type(self)):
            raise TypeError
        return items

    def add(self, item):
        item = self._type_check(item)
        self._set.add(item)

    def __add__(self, other):
        union = GdcApiNodeSet(self._element_type)
        union |= self
        if isinstance(other, self._element_type):
            union.add(other)
        elif isinstance(other, type(self)):
            union |= other
        else:
            raise TypeError
        return union

    def __iadd__(self, other):
        self = self + other
        return self

    def __or__(self, other):
        other = self._array_type_check(other)
        union = GdcApiNodeSet(self._element_type)
        union._set = self._set | other._set
        return union

    def __ior__(self, other):
        self = self | other
        return self

    def __and__(self, other):
        other = self._array_type_check(other)
        intersection = GdcApiNodeSet(self._element_type)
        intersection._set = self._set & other._set
        return intersection

    def _iand__(self, other):
        self = self & other
        return self

    def __sub__(self, other):
        other = self._array_type_check(other)
        diff = GdcApiNodeSet(self._element_type)
        diff._set = self._set - other._set
        return diff

    def _isub__(self, other):
        self = self - other
        return self

class GdcApiFieldSet(GdcApiNodeSet):
    def __init__(self):
        super().__init__(GdcApiField)

class GdcApiGroupSet(GdcApiNodeSet):
    def __init__(self):
        super().__init__(GdcApiGroup)

class GdcApiQueryFilter(object):

    def __init__(self):
        self._filter = {}

    @property
    def filter(self):
        return self._filter

    def __and__(self, other):
        conj = GdcApiQueryFilter()
        conj._filter = self._binary_op(other, 'and')
        return conj

    def __rand__(self, other):
        return self.__and__(other)

    def __iand__(self, other):
        self._filter = self._binary_op(other, 'and')
        return self

    def __or__(self, other):
        disj = GdcApiQueryFilter()
        disj._filter = self._binary_op(other, 'or')
        return disj

    def __ror__(self, other):
        return self.__or__(other)

    def __ior__(self, other):
        self._filter = self._binary_other(other, 'or')
        return self

    def _binary_op(self, other, op):
        if isinstance(other, GdcApiQueryFilter):
            content = [self._filter, other._filter]
        elif isinstance(other, GdcApiField):
            field_exists = other()
            content = [self._filter, field_exists]
        else:
            raise TypeError

        _filter = {
                    'op'      : op,
                    'content' : content
                  }
        return _filter

    def field_range(field,
                    lb,
                    ub,
                    strict_lb = False,
                    strict_ub = False):
        if strict_ub:
            _ub = field < ub
        else:
            _ub = field <= ub
        if strict_lb:
            _lb = field > lb
        else:
            _lb = field >= lb
        self &= ( _lb & _ub )
