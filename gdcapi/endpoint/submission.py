from gdcapi.endpoint.base import GdcEndpoint

class SubmissionBase(GdcEndpoint):
    def __init__(self, api_root, **kwargs):
        super().__init__(api_root, 'submission')

class Submission(SubmissionBase):
    def __init__(self, api_root):
        super().__init__(api_root)

