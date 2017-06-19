class GdcApiGroup(object):

    _fields = []
    _groups = []

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def fields(self):
        return self._fields

    @property
    def groups(self):
        return self._groups
