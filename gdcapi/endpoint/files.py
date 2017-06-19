import os

from gdcapi.endpoint.base import GdcEndpoint

class FilesBase(GdcEndpoint):
    def __init__(self, api_root, **kwargs):
        super().__init__(api_root, 'files')

class Files(FilesBase):
    def __init__(self, api_root):
        super().__init__(api_root)

