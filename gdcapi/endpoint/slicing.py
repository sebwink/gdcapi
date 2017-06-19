from gdcapi.endpoint.base import GdcEndpoint

class SlicingBase(GdcEndpoint):
    def __init__(self, api_root, **kwargs):
        super().__init__(api_root, 'slicing')

class Slicing(SlicingBase):
    def __init__(self, api_root):
        super().__init__(api_root)

