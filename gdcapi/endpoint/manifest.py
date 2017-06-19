from gdcapi.endpoint.base import GdcEndpoint

class ManifestBase(GdcEndpoint):
    def __init__(self, api_root, **kwargs):
        super().__init__(api_root, 'manifest')

class Manifest(ManifestBase):
    def __init__(self, api_root):
        super().__init__(api_root)

