from gdcapi.endpoint.base import GdcEndpoint

class DataBase(GdcEndpoint):
    def __init__(self, api_root, **kwargs):
        super().__init__(api_root, 'data')

class Data(DataBase):
    def __init__(self, api_root, log_fp):
        super().__init__(api_root, log_fp)

