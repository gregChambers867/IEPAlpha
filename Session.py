__author__ = 'gregChambers'
class UUIDCatalog(object):

    def __init__(self):
        """
        : attribute major : string
        : attribute minor : string
        : attribute u_u_i_d : string
        """
        self.major = None
        self.minor = None
        self.u_u_i_d = None




class Configuration(object):

    def __init__(self):
        """
        : attribute expiration : string
        : attribute value : string
        : attribute key : string
        : attribute timestamp : string
        """
        self.expiration = None
        self.value = None
        self.key = None
        self.timestamp = None


class SessionMetadata(object):

    def __init__(self):
        """
        : attribute transaction_i_d : string
        : attribute timestamp : string
        : attribute expiration : string
        """
        self.transaction_i_d = None
        self.timestamp = None
        self.expiration = None


class BaseClass(object):

    def __init__(self):
        """
        : attribute u_u_i_d_catalog : array
        : attribute configuration : array
        : attribute session_i_d : string
        : attribute session_metadata : array
        """
        self.u_u_i_d_catalog = None
        self.configuration = None
        self.session_i_d = None
        self.session_metadata = None

    def __json__(self,request):
        return dict(uuid = self.u_u_i_d_catalog)