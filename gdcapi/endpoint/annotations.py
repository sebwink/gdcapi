import os

from gdcapi.endpoint.base import GdcEndpoint

class AnnotationsBase(GdcEndpoint):
    def __init__(self, api_root, **kwargs):
        super().__init__(api_root, 'annotations')

class Annotations(AnnotationsBase):
    def __init__(self, api_root):
        super().__init__(api_root)

