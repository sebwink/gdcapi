from gdcapi.endpoint.base import GdcEndpoint, DEFAULT_API_ROOT

class FilesBase(GdcEndpoint):
    def __init__(self, api_root, **kwargs):
        super().__init__(api_root, 'files')

class Files(FilesBase):
    def __init__(self, api_root = DEFAULT_API_ROOT):
        super().__init__(api_root)

