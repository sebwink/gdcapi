'''

'''
from gdcapi.endpoint.status import StatusBase, Status
from gdcapi.endpoint.projects import ProjectsBase, Projects
from gdcapi.endpoint.cases import CasesBase, Cases
from gdcapi.endpoint.files import FilesBase, Files
from gdcapi.endpoint.annotations import AnnotationsBase, Annotations
from gdcapi.endpoint.data import DataBase, Data
from gdcapi.endpoint.manifest import ManifestBase, Manifest
from gdcapi.endpoint.slicing import SlicingBase, Slicing
from gdcapi.endpoint.submission import SubmissionBase, Submission

import gdcapi.response
import gdcapi.database

# class 

class GdcApi(object): #, Meta=GdcApiValidation):
    '''
    This class provides a basic interface to the Genomics
    Data Commons (GDC) API.

    https://portal.gdc.cancer.gov/.

    https://docs.gdc.cancer.gov/API/Users_Guide/Getting_Started/

    >>> api = GdcApi()
    >>> api.root
    'https://api.gdc.cancer.gov'
    >>> status = api.query(api.status)
    >>> type(status)
    <class 'dict'>
    >>> api.status.query() == status
    True
    >>> api.query('status') == status
    True
    '''
    _api_root = 'https://api.gdc.cancer.gov'

    def __init__(self,
                 version = 'latest',
                 legacy = False,
                 status_endpoint = StatusBase,
                 projects_endpoint = ProjectsBase,
                 cases_endpoint = CasesBase,
                 files_endpoint = FilesBase,
                 annotations_endpoint = AnnotationsBase,
                 data_endpoint = DataBase,
                 manifest_endpoint = ManifestBase,
                 slicing_endpoint = SlicingBase,
                 submission_endpoint = SubmissionBase,
                 **kwargs):
        '''
        Specify the data version and whether you want access
        legacy data, as well as a log file.

        Args:
            version (str): Version of API to use
            legacy (bool): Whether to use legacy archive
            status_endpoint (StatusBase): Status endpoint
            projects_endpoint (ProjectsBase): Projects endpoint
            cases_endpoint (CasesBase): Cases endpoint
            files_endpoint (FilesBase): Files endpoint
            annotations_endpoint (AnnotationsBase): Annotations endpoint
            data_endpoint (DataBase): Data endpoint
            manifest_endpoint (ManifestBase): Manifest endpoint
            slicing_endpoint (SlicingBase): Slicing endpoint
            submission_endpoint (SubmissionBase): Submission endpoint

        Attributes:

            status (StatusBase): Status endpoint


        >>> api = GdcApi()
        >>> api.root
        'https://api.gdc.cancer.gov'
        >>> apiv0 = GdcApi('v0')
        >>> apiv0.root
        'https://api.gdc.cancer.gov/v0'
        >>> api_legacy = GdcApi(legacy=True)
        >>> api_legacy.root
        'https://api.gdc.cancer.gov/legacy'
        >>> apiv0_legacy = GdcApi('v1', True)
        >>> apiv0_legacy.root
        'https://api.gdc.cancer.gov/v1/legacy'
        >>> isinstance(api.cases, CasesBase)
        True
        '''
        if version != 'latest':
            self._api_root += '/'+version
        if legacy:
            self._api_root += '/legacy'

        # endpoints; TODO: sanity checks
        self.status = status_endpoint(self.root, **kwargs.get('status_args', {}))
        self.projects = projects_endpoint(self.root, **kwargs.get('projects_args', {}))
        self.cases = cases_endpoint(self.root, **kwargs.get('cases_args', {}))
        self.files = files_endpoint(self.root, **kwargs.get('files_args', {}))
        self.annotations = annotations_endpoint(self.root, **kwargs.get('annotations_args', {}))
        self.data = data_endpoint(self.root, **kwargs.get('data_args', {}))
        self.manifest = manifest_endpoint(self.root, **kwargs.get('manifest_args', {}))
        self.slicing = slicing_endpoint(self.root, **kwargs.get('sclicing_args', {}))
        self.submission = submission_endpoint(self.root, **kwargs.get('submission_args', {}))

    @property
    def root(self):
        '''
        Get the root url of the specified API.

        Returns:
            str: Root url of the API specified
                 during initialization


        >>> api = GdcApi()
        >>> api.root
        'https://api.gdc.cancer.gov'
        '''
        return self._api_root

    def query(self, endpoint, query={}):
        '''
        Query an endpoint of the API.
        '''
        if isinstance(endpoint, str):
            endpoint = eval('self.'+endpoint)
        return endpoint.query(query)


class GDC(GdcApi):
    '''
    An interface to the Genomics Data Commons (GDC) API
    which provides some predefined utilites and queries.

    https://portal.gdc.cancer.gov/

    https://docs.gdc.cancer.gov/API/Users_Guide/Getting_Started/
    '''
    def __init__(self,
                 version = 'latest',
                 legacy = False):

        super().__init__(version,
                         legacy,
                         status_endpoint = Status,
                         projects_endpoint = Projects,
                         cases_endpoint = Cases,
                         files_endpoint = Files,
                         annotations_endpoint = Annotations,
                         data_endpoint = Data,
                         manifest_endpoint = Manifest,
                         slicing_endpoint = Slicing,
                         submission_endpoint = Submission)

    # ------------------------------------------------------------------------ #

    def list_projects(self):
        '''
        Get a list with all available projects in GDC.
        '''
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

