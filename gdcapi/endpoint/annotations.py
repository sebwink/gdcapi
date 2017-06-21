import os

from gdcapi.endpoint.base import GdcEndpoint, DEFAULT_API_ROOT

class AnnotationsBase(GdcEndpoint):
    def __init__(self, api_root, **kwargs):
        super().__init__(api_root, 'annotations')

class Annotations(AnnotationsBase):
    def __init__(self, api_root = DEFAULT_API_ROOT):
        super().__init__(api_root)

