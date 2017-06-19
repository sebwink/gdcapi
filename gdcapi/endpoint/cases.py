import os

from gdcapi.endpoint.base import GdcEndpoint

class CasesBase(GdcEndpoint):
    def __init__(self, api_root, **kwargs):
        super().__init__(api_root, 'cases')

class Cases(CasesBase):
    def __init__(self, api_root):
        super().__init__(api_root)

