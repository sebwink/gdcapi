import os

from gdcapi.endpoint.base import GdcEndpoint

class ProjectsBase(GdcEndpoint):
    def __init__(self, api_root, **kwargs):
         super().__init__(api_root, 'projects')

class Projects(ProjectsBase):
    def __init__(self, api_root):
        super().__init__(api_root)

