__author__ = 'gregChambers'

class Session(object):

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


class UUIDCatalog(object):

    def __init__(self):
        """
        : attribute major_minors : array
        : attribute u_u_i_d : string
        """
        self.major_minors = None
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


class MajorMinors(object):

    def __init__(self):
        """
        : attribute major : string
        : attribute minor : string
        """
        self.major = None
        self.minor = None


class SessionMetadata(object):

    def __init__(self):
        """
        : attribute transaction_i_d : string
        : attribute timestamp : string
        : attribute ping : string
        """
        self.transaction_i_d = None
        self.timestamp = None
        self.ping = None

