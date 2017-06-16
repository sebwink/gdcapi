import gdcapi.endpoint
import gdcapi.logging
import gdcapi.response
import gdcapi.database

class GdcApi(object):
    _api_root = 'https://api.gdc.cancer.gov'

    def __init__(self, version='latest',
                       legacy=False,
                       log_file=gdcapi.logging.default_log_file):
        if version != 'latest':
            self._api_root += '/'+version
        if legacy:
            self._api_root += '/legacy'

        if log_file:
            self._log_file = open(log_file, 'a')

        # endpoints
        self.status = gdcapi.endpoint.Status(self.api_root, self.log_file)
        self.projects = gdcapi.endpoint.Projects(self.api_root, self.log_file)
        self.cases = gdcapi.endpoint.Cases(self.api_root, self.log_file)
        self.files = gdcapi.endpoint.Files(self.api_root, self.log_file)
        self.annotations = gdcapi.endpoint.Annotations(self.api_root, self.log_file)
        self.data = gdcapi.endpoint.Data(self.api_root, self.log_file)
        self.manifest = gdcapi.endpoint.Manifest(self.api_root, self.log_file)
        self.slicing = gdcapi.endpoint.Slicing(self.api_root, self.log_file)
        self.submission = gdcapi.endpoint.Submission(self.api_root, self.log_file)

    @property
    def api_root(self):
        return self._api_root

    @property
    def log_file(self):
        return self._log_file

    def query(self, endpoint, query={}, as_json=True):
        if isinstance(endpoint, str):
            endpoint = eval('self.'+endpoint)
        return endpoint.query(query, as_json)


class GDC(GdcApi):
    def __init__(self, version='latest',
                       legacy=False,
                       log_file=gdcapi.logging.default_log_file):
        super().__init__(version, legacy, log_file)

    # ------------------------------------------------------------------------ #

    def list_projects(self):
        num_proj_est = 39
        while True:
            response = self.query(self.projects, {'size': num_proj_est})
            if response['data']['pagination']['total'] <= num_proj_est:
                return response['data']['hits']
            num_proj_est += 39

    def _list_xxx_projects(self, xxx):
        return [ project for project in self.list_projects() if project['project_id'].split('-')[0] == xxx ]

    def list_tcga_projects(self):
        return self._list_xxx_projects('TCGA')

    def list_ccle_projects(self):
        return self._list_xxx_projects('CCLE')

    def list_target_projects(self):
        return self._list_xxx_projects('TARGET')

