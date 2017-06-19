from gdcapi.endpoint.base import GdcEndpoint

class StatusBase(GdcEndpoint):
    def __init__(self, api_root, **kwargs):
        super().__init__(api_root, 'status')

class Status(StatusBase):
    def __init__(self, api_root):
        super().__init__(api_root)

    def _key(self, key):
        status = self.query()
        return status[key]

    @property
    def commit(self):
        return self._key('commit')

    @property
    def data_release(self):
        return self._key('data_release')

    @property
    def status(self):
        return self._key('status')

    @property
    def tag(self):
        return self._key('tag')

    @property
    def version(self):
        return self._key('version')

