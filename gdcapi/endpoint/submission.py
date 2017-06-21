from gdcapi.endpoint.base import GdcEndpoint, DEFAULT_API_ROOT

class SubmissionBase(GdcEndpoint):
    def __init__(self, api_root, **kwargs):
        super().__init__(api_root, 'submission')

class Submission(SubmissionBase):
    def __init__(self, api_root = DEFAULT_API_ROOT): 
        super().__init__(api_root)

