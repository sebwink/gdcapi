from gdcapi.endpoint.base import GdcEndpoint, DEFAULT_API_ROOT

class ManifestBase(GdcEndpoint):
    def __init__(self, api_root, **kwargs):
        super().__init__(api_root, 'manifest')

class Manifest(ManifestBase):
    def __init__(self, api_root = DEFAULT_API_ROOT): 
        super().__init__(api_root)

